# conftest.py

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    print("=== RT Result Start ===")
    
    if 'passed' in terminalreporter.stats:
        print('Passed amount:', len(terminalreporter.stats['passed']))
    else:
        print('Passed amount:', 0)
    
    if 'failed' in terminalreporter.stats:
        print('Failed amount:', len(terminalreporter.stats['failed']))
    else:
        print('Failed amount:', 0)
        
    print("=== RT Result End ===")
#     print('xfailed amount:', len(terminalreporter.stats['xfailed']))
#     print('skipped amount:', len(terminalreporter.stats['skipped']))

#     duration = time.time() - terminalreporter._sessionstarttime
#     print('duration:', duration, 'seconds')