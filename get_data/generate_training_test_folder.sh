for data_type in training test
do
  mkdir ${data_type}
  cd ${data_type}

  for floor in {0..10}
  do
    mkdir "${floor}f"
  done

  cd ..
done