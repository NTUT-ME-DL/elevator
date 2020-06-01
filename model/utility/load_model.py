def load_model(architecture_file_path, model_weights_file_path):
  with open("{}.json".format(architecture_file_path), "r") as json_file:
    model = model_from_json(json_file.read())

  model.load_weights("{}.h5".format(model_weights_file_path))
  model.compile(loss="categorical_crossentropy",
                optimizer="adam",
                metrics=["categorical_accuracy"])
              
  return model