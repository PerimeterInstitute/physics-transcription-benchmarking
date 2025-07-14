from test_classes.Test import Test
from models.WhisperCPP import WhisperCPP
from models.Parakeet import Parakeet
model_1 = WhisperCPP("whisper_CPP", "whisper.cpp/", {})

model_2 = Parakeet()

test = Test(model_array=[model_1,model_2])

test.run(run_name="full_test",
         dataset_path="datasets/dev_dataset/",
         run_num=1)

test.free()