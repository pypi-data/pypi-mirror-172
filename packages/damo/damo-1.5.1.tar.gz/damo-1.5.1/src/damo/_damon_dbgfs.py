#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

"""
Contains core functions for DAMON debugfs control.
"""

import os
import subprocess

import _damo_fs
import _damo_schemes_input
import _damon

debugfs = '/sys/kernel/debug'
debugfs_damon = os.path.join(debugfs, 'damon')
debugfs_version = os.path.join(debugfs_damon, 'version')
debugfs_attrs = os.path.join(debugfs_damon, 'attrs')
debugfs_record = os.path.join(debugfs_damon, 'record')
debugfs_schemes = os.path.join(debugfs_damon, 'schemes')
debugfs_target_ids = os.path.join(debugfs_damon, 'target_ids')
debugfs_init_regions = os.path.join(debugfs_damon, 'init_regions')
debugfs_monitor_on = os.path.join(debugfs_damon, 'monitor_on')

def turn_damon(on_off, kdamonds):
    return _damo_fs.write_files({debugfs_monitor_on: on_off})

def is_damon_running():
    result = _damo_fs.read_files_recursive(debugfs_damon)
    return result['monitor_on'].strip() == 'on'

feature_supports = None

def feature_supported(feature):
    if feature_supports == None:
        initialize()

    return feature_supports[feature]

def values_for_restore(filepath, read_val):
    if read_val == '':
        return '\n'
    if os.path.basename(filepath) == 'target_ids' and read_val == '42\n':
        return 'paddr\n'
    return read_val

'''Return value to write back to the filepath for restoring, and error'''
def read_value_for_restore(filepath):
    err = True
    read_val, err = _damo_fs.read_file(filepath)
    if err != None:
        return None, err
    err = None
    return values_for_restore(filepath, read_val), err

def test_debugfs_file(path, input_str, expected):
    orig_val, err = read_value_for_restore(path)
    if err != None:
        return False
    err = _damo_fs.write_file(path, input_str)
    if err != None:
        return False
    content, err = _damo_fs.read_file(path)
    if err != None:
        return False
    if content == expected:
        passed = True
    else:
        passed = False
    err = _damo_fs.write_file(path, orig_val)
    if err != None:
        return False
    return passed

def test_debugfs_file_schemes(nr_fields):
    input_str = ' '.join(['1'] * nr_fields)
    expected = '%s 0 0\n' % input_str

    return test_debugfs_file(debugfs_schemes, input_str, expected)

def test_debugfs_file_schemes_stat_extended(nr_fields):
    input_str = ' '.join(['1'] * nr_fields)
    expected = '%s 0 0 0 0 0\n' % input_str

    return test_debugfs_file(debugfs_schemes, input_str, expected)

def test_init_regions_version(paddr_supported):
    # Save previous values
    orig_target_ids, err = read_value_for_restore(debugfs_target_ids)
    if err != None:
        raise Exception('debugfs target_ids read failed')
    orig_init_regions = read_value_for_restore(debugfs_init_regions)
    if err != None:
        raise Exception('debugfs init_regions read failed')

    # Test
    if paddr_supported:
        err = _damo_fs.write_file(debugfs_target_ids, 'paddr\n')
        if err != None:
            raise Exception(err)
        v1_input = '42 100 200'
    else:
        err = _damo_fs.write_file(debugfs_target_ids, '%d\n' % os.getpid())
        if err != None:
            raise Exception(err)
        v1_input = '%d 100 200' % os.getpid()

    # We check if the write was success below anyway, so ignore error
    err = _damo_fs.write_file(debugfs_init_regions, v1_input)
    read_val, err = _damo_fs.read_file(debugfs_init_regions)
    if err != None:
        raise Exception(err)
    if read_val.strip() == v1_input:
        version = 1
    else:
        version = 2

    # Previous value might be invalid now (e.g., process terminated), so ignore
    # error
    err = _damo_fs.write_file(debugfs_target_ids, orig_target_ids)
    err = _damo_fs.write_file(debugfs_init_regions, orig_init_regions)

    return version

def update_supported_features():
    global feature_supports
    if feature_supports != None:
        return None
    feature_supports = {x: False for x in _damon.features}

    err = set_damon_debugfs_paths()
    if err != None:
        return err

    if is_damon_running():
        return 'debugfs feature update cannot be done while DAMON running'

    if debugfs_record != None:
        feature_supports['record'] = True
    if debugfs_schemes != None:
        feature_supports['schemes'] = True

    # virtual address space has supported since the beginning
    feature_supports['vaddr'] = True
    if test_debugfs_file(debugfs_target_ids, 'paddr\n', '42\n'):
        feature_supports['paddr'] = True

    if debugfs_init_regions != None:
        feature_supports['init_regions'] = True
        init_regions_version = test_init_regions_version(
                feature_supports['paddr'])
        if init_regions_version == 2:
            feature_supports['init_regions_target_idx'] = True

    if debugfs_schemes != None:
        if test_debugfs_file_schemes(9):
            feature_supports['schemes_speed_limit'] = True
        elif test_debugfs_file_schemes(12):
            feature_supports['schemes_speed_limit'] = True
            feature_supports['schemes_prioritization'] = True
        elif test_debugfs_file_schemes(17):
            feature_supports['schemes_speed_limit'] = True
            feature_supports['schemes_prioritization'] = True
            feature_supports['schemes_wmarks'] = True
        elif test_debugfs_file_schemes(18):
            feature_supports['schemes_speed_limit'] = True
            feature_supports['schemes_prioritization'] = True
            feature_supports['schemes_wmarks'] = True
            feature_supports['schemes_quotas'] = True
        elif test_debugfs_file_schemes_stat_extended(18):
            feature_supports['schemes_speed_limit'] = True
            feature_supports['schemes_prioritization'] = True
            feature_supports['schemes_wmarks'] = True
            feature_supports['schemes_quotas'] = True
            feature_supports['schemes_stat_succ'] = True
            feature_supports['schemes_stat_qt_exceed'] = True
    return None

def set_damon_debugfs_paths():
    'Set global variables for DAMON debugfs path.  Return error if failed'
    global debugfs_damon
    global debugfs_version
    global debugfs_attrs
    global debugfs_record
    global debugfs_schemes
    global debugfs_target_ids
    global debugfs_init_regions
    global debugfs_monitor_on

    if not os.path.isdir(debugfs_damon):
        return 'damon debugfs dir (%s) not found' % debugfs_damon

    for f in [debugfs_version, debugfs_attrs, debugfs_record, debugfs_schemes,
            debugfs_target_ids, debugfs_init_regions, debugfs_monitor_on]:
        # f could be None if this function is called before
        if f == None:
            continue
        if not os.path.isfile(f):
            if f == debugfs_version:
                debugfs_version = None
            elif f == debugfs_record:
                debugfs_record = None
            elif f == debugfs_schemes:
                debugfs_schemes = None
            elif f == debugfs_init_regions:
                debugfs_init_regions = None
            else:
                return 'damon debugfs file (%s) not found' % f
    return None

def initialize(skip_dirs_population=False):
    err = update_supported_features()
    if err:
        return err
    return None

def attr_str(attrs):
    return '%s %s %s %s %s ' % (attrs.sample_interval, attrs.aggr_interval,
            attrs.regions_update_interval, attrs.min_nr_regions,
            attrs.max_nr_regions)

class DebugfsInputs:
    attrs = None
    record = None
    schemes = None

def current_debugfs_inputs():
    debugfs_inputs = DebugfsInputs()

    with open(debugfs_attrs, 'r') as f:
        debugfs_inputs.attrs = f.read().strip()

    if debugfs_record:
        with open(debugfs_record, 'r') as f:
            debugfs_inputs.record = f.read().strip()

    if debugfs_schemes:
        with open(debugfs_schemes, 'r') as f:
            # The last two fields in each line are statistics.
            schemes = [' '.join(x.split()[:-2]) for x in
                    f.read().strip().split('\n')]
            debugfs_inputs.schemes = '\n'.join(schemes)

def apply_debugfs_inputs(debugfs_inputs):
    _damo_fs.write_files([{debugfs_attrs: debugfs_inputs.attrs},
            {debugfs_record: debugfs_inputs.record},
            {debugfs_schemes: debugfs_inputs.schemes}])

def attr_str_ctx(damon_ctx):
    intervals = damon_ctx.intervals
    nr_regions = damon_ctx.nr_regions
    return '%d %d %d %d %d ' % (intervals.sample, intervals.aggr,
            intervals.ops_update, nr_regions.min_nr_regions,
            nr_regions.max_nr_regions)

def get_scheme_version():
    scheme_version = 0
    if feature_supported('schemes_speed_limit'):
        scheme_version = 1
    if feature_supported('schemes_prioritization'):
        scheme_version = 2
    if feature_supported('schemes_wmarks'):
        scheme_version = 3
    if feature_supported('schemes_quotas'):
        scheme_version = 4
    return scheme_version

def damos_to_debugfs_input(damos, sample_interval, aggr_interval,
        scheme_version):
    pattern = damos.access_pattern
    quotas = damos.quotas
    watermarks = damos.watermarks

    max_nr_accesses = aggr_interval / sample_interval
    v0_scheme = '%d\t%d\t%d\t%d\t%d\t%d\t%d' % (
            pattern.min_sz_bytes, pattern.max_sz_bytes,
            int(pattern.min_nr_accesses * max_nr_accesses / 100
                if pattern.nr_accesses_unit == 'percent'
                else pattern.min_nr_accesses),
            int(pattern.max_nr_accesses * max_nr_accesses / 100
                if pattern.nr_accesses_unit == 'percent'
                else pattern.max_nr_accesses),
            (pattern.min_age / aggr_interval if pattern.age_unit == 'usec'
                else pattern.min_age),
            (pattern.max_age / aggr_interval if pattern.age_unit == 'usec'
                else pattern.max_age),
            _damo_schemes_input.damos_action_to_int[damos.action])
    v1_scheme = '%s\t%d\t%d' % (v0_scheme,
            quotas.sz_bytes, quotas.reset_interval_ms)
    v2_scheme = '%s\t%d\t%d\t%d' % (v1_scheme,
            quotas.weight_sz_permil, quotas.weight_nr_accesses_permil,
            quotas.weight_age_permil)
    v3_scheme = '%s\t%d\t%d\t%d\t%d\t%d' % (v2_scheme,
            _damo_schemes_input.text_to_damos_wmark_metric(watermarks.metric),
            watermarks.interval_us, watermarks.high_permil,
            watermarks.mid_permil, watermarks.low_permil)
    v4_scheme = '%s\t' % v0_scheme + '\t'.join('%d' % x for x in [quotas.time_ms,
        quotas.sz_bytes, quotas.reset_interval_ms, quotas.weight_sz_permil,
        quotas.weight_nr_accesses_permil, quotas.weight_age_permil,
        _damo_schemes_input.text_to_damos_wmark_metric(watermarks.metric),
        watermarks.interval_us, watermarks.high_permil, watermarks.mid_permil,
        watermarks.low_permil])

    if scheme_version == 0:
        return v0_scheme
    elif scheme_version == 1:
        return v1_scheme
    elif scheme_version == 2:
        return v2_scheme
    elif scheme_version == 3:
        return v3_scheme
    elif scheme_version == 4:
        return v4_scheme
    else:
        print('Unsupported scheme version: %d' % scheme_version)
        exit(1)

def apply_kdamonds(kdamonds):
    if len(kdamonds) != 1:
        print('Currently only one kdamond is supported')
        exit(1)
    if len(kdamonds[0].contexts) != 1:
        print('currently only one damon_ctx is supported')
        exit(1)
    if len(kdamonds[0].contexts[0].targets) != 1:
        print('currently only one target is supported')
        exit(1)
    ctx = kdamonds[0].contexts[0]

    write_contents = []
    write_contents.append({debugfs_attrs: attr_str_ctx(ctx)})

    target = ctx.targets[0]
    if _damon.target_has_pid(ctx.ops):
        write_contents.append({debugfs_target_ids: '%s' % target.pid})
        tid = target.pid
    else:
        if not feature_supported('paddr'):
            print('paddr is not supported')
            exit(1)
        write_contents.append({debugfs_target_ids: 'paddr\n'})
        tid = 42
    if feature_supported('init_regions_target_idx'):
        tid = 0

    if feature_supported('init_regions'):
        string = ' '.join(['%s %d %d' % (tid, r.start, r.end) for r in
            target.regions])
        write_contents.append({debugfs_init_regions: string})

    if feature_supported('record') and ctx.record_request != None:
        record_file_input = '%s %s' % (ctx.record_request.rfile_buf,
                ctx.record_request.rfile_path)
        write_contents.append({debugfs_record: record_file_input})

    if not debugfs_schemes:
        return _damo_fs.write_files(write_contents)

    scheme_version = get_scheme_version()

    scheme_file_input_lines = []
    for scheme in ctx.schemes:
        scheme_file_input_lines.append(damos_to_debugfs_input(scheme,
            ctx.intervals.sample, ctx.intervals.aggr, scheme_version))
    scheme_file_input = '\n'.join(scheme_file_input_lines)
    if scheme_file_input == '':
        scheme_file_input = '\n'

    write_contents.append({debugfs_schemes: scheme_file_input})
    err = _damo_fs.write_files(write_contents)
    if err:
        print(err)
