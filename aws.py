# day13에 import 시킬것
# print("나 실행되면 안됨")

# def add(a,b):
#     return a + b

# if __name__ =="__main__":
#     print("여기는 진짜 실행되면 안됨")
    # test.py에서는 실행X
    # 직접실행하면 __name__ =="__main__" 이 실행하면서 main
    # 외부에서 실행하면 실행 X
    # critical code는 여기다가 써야 굿


#---------------------------위는 불러오기 예시-------------------------------


#---------------------------객체감지코드-----------------------------

import boto3

def detect_labels_local_file(photo):

    client = boto3.client('rekognition')
   
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
    
    result = []

    for label in response["Labels"]:
        name = label["Name"]
        confidence = label["Confidence"]

        result.append(f"{name} : {confidence:.2f}%")

    r = "<br/>".join(map(str, result))
    return r



def compare_faces(sourceFile, targetFile):

    client = boto3.client('rekognition')

    imageSource = open(sourceFile, 'rb')
    imageTarget = open(targetFile, 'rb')

    response = client.compare_faces(SimilarityThreshold=0,
                                    SourceImage={'Bytes': imageSource.read()},
                                    TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        similarity = faceMatch['Similarity']
            
    imageSource.close()
    imageTarget.close()
    return  f"동일 인물일 확률은: {similarity:.2f}%입니다."




