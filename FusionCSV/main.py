import numpy as np
import csv

SplitCam1 = []
SplitCam2 = []
SplitCam3 = []
SplitCam4 = []
Output_data = []
j=0
nom_fichier = 'Output.csv'

# L'axe X représente la direction horizontale.  >
# L'axe Y représente la direction verticale. /\
# L'axe Z représente la direction perpendiculaire au plan XY (c'est-à-dire la profondeur). o

def positionnement(AB,BC,CA):
    cos_A = (CA**2 + AB**2 - BC**2) / (2 * CA * AB)
    cos_B = (-CA**2 + BC**2 + AB**2) / (2 * BC * AB)
    cos_C = (BC**2 + CA**2 - AB**2) / (2 * BC * CA)

    angle_A = np.arccos(cos_A)
    angle_B = np.arccos(cos_B)
    angle_C = np.arccos(cos_C)

    # Convertir les angles en degrés si nécessaire
    angle_A_degrees = np.degrees(angle_A)
    angle_B_degrees = np.degrees(angle_B)
    angle_C_degrees = np.degrees(angle_C)

    #print("Angle A : " + str(round(angle_A_degrees, 1)))

    return angle_A_degrees

def rx(cos_theta, sin_theta):
    rotation_matrix = [[1,0,0],[0,cos_theta,-sin_theta],[0,sin_theta,cos_theta]]
    return rotation_matrix

def ry(cos_theta, sin_theta):
    rotation_matrix = [[cos_theta,0,sin_theta],[0,1,0],[-sin_theta,0,cos_theta]]
    return rotation_matrix

def rz(cos_theta, sin_theta):
    rotation_matrix = [[cos_theta,-sin_theta,0],[sin_theta,cos_theta,0],[0,0,1]]
    return rotation_matrix

# main

#position cam 2
AB_cam2 = 3.32 # Longueur du côté AB
BC_cam2 = 2.52  # Longueur du côté BC
CA_cam2 = 2.33  # Longueur du côté CA
angle_radians_cam2 = np.radians(positionnement(AB_cam2,BC_cam2,CA_cam2)) # calcul de l'angle entre la cam 2 et la cam 3

#position cam 1
AB_cam1 = 3.28  # Longueur du côté AB
BC_cam1 = 2.12  # Longueur du côté BC
CA_cam1 = 2.65  # Longueur du côté CA
angle_radians_cam1 = np.radians(positionnement(AB_cam1,BC_cam1,CA_cam1)) #calcul de l'angle entre la cam 4 et la cam 1


#with open('1LBR_1684830276_ID_Emilio_cam_1.csv', 'r') as cam1, \
#     open('1LBR_1684830276_ID_Emilio_cam_2.csv', 'r') as cam2, \
#     open('1LBR_1684830276_ID_Emilio_cam_3.csv', 'r') as cam3, \
#     open('1LBR_1684830276_ID_Emilio_cam_4.csv', 'r') as cam4, \
#     open(nom_fichier, 'w', newline='') as fichier_csv :


with open('chessboard_1685968291_ID_N o_cam_1.csv', 'r') as cam1, \
     open('chessboard_1685968291_ID_N o_cam_2.csv', 'r') as cam2, \
     open('chessboard_1685968291_ID_N o_cam_3.csv', 'r') as cam3, \
     open('chessboard_1685968291_ID_N o_cam_4.csv', 'r') as cam4, \
     open(nom_fichier, 'w', newline='') as fichier_csv:

    for LigneCam1, LigneCam2, LigneCam3, LigneCam4 in zip(cam1, cam2, cam3, cam4):
        # Traitez les lignes des deux fichiers simultanément

        SplitCam1 = LigneCam1.split(",")
        SplitCam2 = LigneCam2.split(",")
        SplitCam3 = LigneCam3.split(",")
        SplitCam4 = LigneCam4.split(",")
        #print("---------------Frame n°"+str(j))
        min_length = min(len(SplitCam1), len(SplitCam2), len(SplitCam3), len(SplitCam4))

        if all(value.strip() == '' for value in SplitCam1[3:min_length:3]) \
                and all(value.strip() == '' for value in SplitCam2[3:min_length:3]) \
                and all(value.strip() == '' for value in SplitCam3[3:min_length:3]) \
                and all(value.strip() == '' for value in SplitCam4[3:min_length:3]):
            continue

        for i in range(0, min_length, 3):
            #print("Valeur n°"+str(i))

            coordinates_cam1 = np.array([float(SplitCam1[i - 3]), float(SplitCam1[i - 2]), float(SplitCam1[i - 1])])
            new_coordinates_cam1 = np.dot(ry(np.cos(angle_radians_cam1), np.sin(angle_radians_cam1)),coordinates_cam1)
            moyenneX = ((float(SplitCam4[i - 3]) + float(new_coordinates_cam1[0])) / 2)

            #print("Valeurs : Cam4=" + str(SplitCam4[i - 3]) + " Cam1 anciene valeur="+str(SplitCam1[i - 3])+" Nouvelle valeur ="+str(new_coordinates_cam1[0]))
            #print("Moyenne X : " + str(moyenneX))

            moyenneY = ((float(SplitCam1[i-2])+float(SplitCam2[i-2])+float(SplitCam3[i-2])+float(SplitCam4[i-2])) / 4)

            #print("Moyenne Y : " + str(moyenneY))

            coordinates_cam2 = np.array([float(SplitCam2[i-3]), float(SplitCam2[i-2]), float(SplitCam2[i-1])])
            new_coordinates_cam2 = np.dot(ry(np.cos(angle_radians_cam2), np.sin(angle_radians_cam2)), coordinates_cam2)
            moyenneZ = ((float(SplitCam3[i - 3]) + float(new_coordinates_cam2[0]))/2)

            #print("Valeurs : Cam4=" + str(SplitCam3[i - 3]) + " Cam2 Anciene valeur="+str(SplitCam2[i-3])+" Nouvelle valeur ="+str(new_coordinates_cam2[0]))
            #print("Moyenne Z : " + str(moyenneZ))

            Output_data.append(round(float(SplitCam4[i - 3]), 4))
            Output_data.append(round(moyenneY, 4))
            Output_data.append(round(float(SplitCam3[i - 3]), 4))

        writer = csv.writer(fichier_csv)
        writer.writerow(Output_data)
        Output_data = []
        j=j+1

print("Nombre de frames : "+str(j))


