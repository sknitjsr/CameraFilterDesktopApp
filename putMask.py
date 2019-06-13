import  cv2
def put_mask(faces ,s_img,l_img,x,y,w,h):
 try :
    if len(faces) > 0:
        # For Mask
        x_offset = faces[0][0]
        y_offset = faces[0][1]

        face_width = w
        face_height = h

        mst_width = int(face_width)
        mst_height = int(face_height)

        s_img = cv2.resize(s_img, (mst_width, mst_height))

        y1, y2 = y_offset, y_offset + s_img.shape[0]
        x1, x2 = x_offset, x_offset + s_img.shape[1]

        alpha_s = s_img[:, :, 3] / 255.0
        # print(alpha_s)
        alpha_l = 1.0 - alpha_s

        # for x,y,w,h in faces:
        #     cv2.rectangle(l_img, (x, y), (x + w, y + h), (255, 0, 0), 5)

        for c in range(0, 3):
            l_img[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] + alpha_l * l_img[y1:y2, x1:x2, c])
        # for x, y, w, h in faces:
        #     l_img[y:y + s_img.shape[0], x:x + s_img.shape[1]] = s_img

        return l_img
 except :
     print("errror")
