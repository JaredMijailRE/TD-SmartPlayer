import audio_capture
import mfcc
import tflite_runtime
import kws_model


interpreter = tflite_runtime.Interpreter(kws_model.model)
interpreter.allocate_tensors()


while True:
    audio = audio_capture.record()
    features = mfcc.compute(audio)


    input = interpreter.tensor(interpreter.get_input_details()[0]['index'])()
    input[:] = features


    interpreter.invoke()
    output = interpreter.get_output_details()[0]['index']
    scores = interpreter.tensor(output)()[0]


    label = scores.argmax()
    print("Detected:", label)