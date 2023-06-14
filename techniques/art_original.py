def apply_art(test_function, art_test_cases):
    test_results = []

    passed_tests = 0
    failed_tests = 0

    for i, value in enumerate(art_test_cases):
        x = value[0]
        y = value[1]
        input_data = (x, y)
        expected_output = x + y if x + y != 0 else (y - x if y > 0 else x - y)
        expected_output = expected_output - x if x > 0 else expected_output + x
        output = test_function(*input_data)

        test_passed = output == expected_output
        if test_passed:
            passed_tests += 1
        else:
            failed_tests += 1
            
        test_results.append({'x': input_data[0], 'y': input_data[1], 'z': output})

    return [test_results, passed_tests, failed_tests]