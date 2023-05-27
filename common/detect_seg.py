
from common.yolo_ import yolo_instance
ys = yolo_instance()

async def detect_person_img(imgData, debug=False):
    """
    이미지에서 사람을 검출한다.
    data[0] : index
    data[1] : ret
    data[2] : img
    ys : yolo_segmentation 객체

    return : 사람 검출된 이미지 / 검출된 사람이 없으면 None
    """
    import cv2
    img = imgData[2]

    # print(111)
    bboxes, classes, segmentations, scores = ys.detect(img)
    # print(222)  # 위에 detect되는 개체도 없으면 이 코드 라인이 실행이 안됨.

    count = 0
    for bbox, class_id, seg, score in zip(bboxes, classes, segmentations, scores):
        # print("bbox:", bbox, "class id:", class_id, "seg:", seg, "score:", score)

        # class id 0은 사람
        if class_id == 0:    
            count += 1
            (x, y, x2, y2) = bbox
            
            cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 2)

            cv2.polylines(img, [seg], True, (0, 0, 255), 4)

            cv2.putText(img, str(class_id), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    
    # 사람 한번도 검출 안된거면 None 리턴
    if count == 0:
        return None

    if debug:
        cv2.imwrite(f'webcam {imgData[0]} seg.jpg', img)
    return img