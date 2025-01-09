#!/bin/bash

echo "Running all tests..."

# Run all tests under the backend/tests directory
python -m unittest discover -s backend/tests -p "*.py"

# Capture the exit status of the tests
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "All tests passed successfully! 🎉"
else
    echo "Some tests failed. Check the output above for details. ❌"
fi

exit $STATUS
