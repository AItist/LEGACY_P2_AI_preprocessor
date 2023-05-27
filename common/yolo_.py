def yolo_instance():
    """
    yolo 인스턴스 생성
    """
    from yolo_segmentation import YOLOSegmentation

    ys = YOLOSegmentation("yolov8n-seg.pt")
    # ys = YOLOSegmentation("yolov8s-seg.pt")

    # ys.detect
    return ys