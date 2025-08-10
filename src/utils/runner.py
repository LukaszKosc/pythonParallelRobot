import os
import sys
import time

from datetime import datetime
from pathlib import Path
from multiprocessing import Pool
from os.path import sep
from robot import run
from robot import rebot
from robot.running.builder.builders import TestSuiteBuilder
from typing import List


__TESTS_DIR_NAMES = ['test', 'tests']
__TESTS_DIRECTORY = [str(item) for item in Path(__file__).parent.parent.parent.iterdir() if any([_it in item.name for _it in __TESTS_DIR_NAMES])]
TEST_CASE_NAME_SEPARATOR = ": "
TIMEOUT_TO_STOP_EXECUTION = None
PROCESSES_RESULTS = []


def get_cmd_args():
    arg_vector = sys.argv
    outputdir = '.'
    msg = 'Provided too many (more than 1) times parameter "{0}" or "{1}". Only 1 supported. Please fix.'
    single_occurrence_params = [('-i', '--include'), ('-e', '--exclude'), ('-d', '--outputdir')]
    for _s, _l in single_occurrence_params:
        if arg_vector.count(_s) > 1 or arg_vector.count(_l) > 1:
            raise ValueError(msg.format(_s, _l))
    
    if any(i in arg_vector for i in ['-i', '--include']):
        include_tags = arg_vector[(arg_vector.index('-i') or arg_vector.index('--include')) + 1]
    if any(i in arg_vector for i in ['-e', '--exclude']):
        exclude_tags = arg_vector[(arg_vector.index('-e') or arg_vector.index('--exclude')) + 1]
    if any(i in arg_vector for i in ['-d', '--outputdir']):
        outputdir = arg_vector[(arg_vector.index('-d') or arg_vector.index('--outputdir')) + 1]
    
    if not outputdir.endswith(sep):
        outputdir += sep

    return {
        'include_tags': include_tags,
        'exclude_tags': exclude_tags,
        'outputdir': outputdir,
        }


def merge_results(outputdir: str):
    output_xml_files = [str(file) for file in Path(outputdir).iterdir() if file.name.endswith('_output.xml')]
    
    target_dir = f'merged_{outputdir}'
    os.makedirs(target_dir, exist_ok=True)
    
    with open(f'{target_dir}merging_results_stdout.txt', 'w') as stdout:
        rebot(
            *output_xml_files, 
            name=f'[{datetime.now():%Y-%m-%d %H:%M:%S}] - All tests execution', 
            log='merged_log', 
            report='merged_report', 
            output='merged_output', 
            outputdir=target_dir, 
            stdout=stdout
            )
    print(f'Finished execution with results in "{target_dir}" directory')


def run_tests(group_name: str, tests: List[str], output_dir: str):
    group_name_underscore = group_name.lower().replace(' ', '_')
    os.makedirs(output_dir, exist_ok=True)
    with open(f'{output_dir}{group_name_underscore}_stdout.txt', 'w') as stdout:
        sys.__stdout__ = stdout  # trick allowing to remove from stdout also 'Log To Console' results
        exec_status = run(
            *__TESTS_DIRECTORY,
            test=tests,
            output=f'{group_name_underscore}_output.xml', 
            report=f'{group_name_underscore}_report.html', 
            log=f'{group_name_underscore}_log.html', 
            outputdir=output_dir.lower(), 
            splitlog=True,
            name=group_name,
            stdout=stdout
            )
    return {group_name: exec_status}


def get_tests(include_tags: str, exclude_tags: str= ''):
    suite = TestSuiteBuilder().build(*__TESTS_DIRECTORY)
    suite.filter(included_tags=include_tags, excluded_tags=exclude_tags)
    tests_groups = {}
    for i in suite.all_tests:
        t_name = i.name
        if TEST_CASE_NAME_SEPARATOR not in t_name:
            # raise ValueError(f'Test Case "{t_name}" does not include required SEPARATOR "{TEST_CASE_NAME_SEPARATOR}".')
            print(f'Test Case "{t_name}" does not include required SEPARATOR "{TEST_CASE_NAME_SEPARATOR}".')
            print('will be skipped - fix it if you like to execute it')
        else:
            t_group_name, _ = t_name.split(TEST_CASE_NAME_SEPARATOR)
            test_group = t_group_name
            if t_name.startswith(f"{test_group}{TEST_CASE_NAME_SEPARATOR}"):
                if test_group not in tests_groups.keys():
                    tests_groups[test_group] = [t_name]
                else:
                    tests_groups[test_group].append(t_name)
    return tests_groups


def finish_process_callback(result):
    for result_item in result:
        print('Result from process:', result_item, flush=True)
        PROCESSES_RESULTS.append(result_item)


if __name__ == '__main__':
    robot_args = get_cmd_args()
    tests = get_tests(robot_args['include_tags'], robot_args['exclude_tags'])
    start = time.perf_counter()
    
    tests_groups_count = len(tests.keys())
    if tests_groups_count < 1:
        raise ValueError('Unfortunately could not find any test case to execute. Please verify if names are ok.')
    
    with Pool(processes=tests_groups_count) as pool:
        outputdir = robot_args['outputdir']
        run_tests_args = [(group_name, tests[group_name], outputdir) for group_name in tests]
    
        result = pool.starmap_async(run_tests, run_tests_args, callback=finish_process_callback)
        result.wait(timeout=TIMEOUT_TO_STOP_EXECUTION)

    if len(PROCESSES_RESULTS):    
        merge_results(outputdir)
    elapsed = time.perf_counter() - start
    msg = f"{__file__} executed in {elapsed:0.2f} seconds."
    print(msg)
