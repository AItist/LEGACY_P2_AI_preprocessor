import webcam_list



if __name__ == "__main__":
    webcam_lst = webcam_list.get_all_webcams()
    webcam_lst = webcam_list.get_available_webcams(webcam_lst)

    # print(webcam_lst)

    for index, camIndex in webcam_lst.items():
        print(index, camIndex)