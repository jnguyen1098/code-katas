CODE="packet.py"
TEST="test_packet.py"

./"$TEST" && ./lint_py.sh "$CODE" && ./lint_py.sh "$TEST"
