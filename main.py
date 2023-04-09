from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import cv2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file attached"})
    file = request.files['file']
    Hello = { "Message": "Success"}
    file.save('data.jpeg')
    return jsonify(Hello)


@app.route('/result', methods=['GET'])
def data_fetch():
	Known_distance = 76.2
	Known_width = 14.3
	face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):
		focal_length = (width_in_rf_image * measured_distance) / real_width
		return focal_length

	def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
		distance = (real_face_width * Focal_Length)/face_width_in_frame
		return distance
	def face_data(image):
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
		face_widths = [0, 0]
		for (x, y, h, w) in faces:
			face_widths.append(w)
		return max(face_widths)
	# reading reference_image from directory
	ref_image = cv2.imread("ref_image.jpeg")
	# find the face width(pixels) in the reference_image
	ref_image_face_width = face_data(ref_image)
	# get the focal by calling "Focal_Length_Finder"
	# face width in reference(pixels),
	# Known_distance(centimeters),
	# known_width(centimeters)
	Focal_length_found = Focal_Length_Finder(
		Known_distance, Known_width, ref_image_face_width)
	print(Focal_length_found)
	# initialize the camera object so that we
	# can get frame from it
		# _, frame = cap.read()
	frame = cv2.imread("data.jpeg")
	face_width_in_frame = face_data(frame)
	# async def get_dist(Focal_length_found, Known_width, face_width_in_frame):
	# 	return await Distance_finder(
	# 		Focal_length_found, Known_width, face_width_in_frame)

	if face_width_in_frame != 0 :
		Distance = Distance_finder(Focal_length_found, Known_width, face_width_in_frame)
	computed_json = {
        "Distance": int(Distance),
        }
	return jsonify(computed_json)
	# cv2.imshow("Frame", frame)
			# cv2.line(frame, (30, 30), (230, 30), RED, 32)
			# cv2.line(frame, (30, 30), (230, 30), BLACK, 28)
	# cap.release()
	# cv2.destroyAllWindows()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
