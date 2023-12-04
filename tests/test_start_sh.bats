#!/usr/bin/env bats

@test "Test llm_server start" {
  export SERVER_TYPE=llm_server
  run ./start.sh
  [ "$status" -eq 0 ]
}

@test "Test my_server start" {
  export SERVER_TYPE=my_server
  run ./start.sh
  [ "$status" -eq 0 ]
}
