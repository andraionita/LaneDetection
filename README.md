# LaneDetection

Aplicatia realizata se bazeaza pe detectarea benzilor de pe strada (lane detection), in timp ce o masina se afla in miscare, folosind deep learning. O procesare si o analiza perfecta a strazii duce la o mai buna acuratete in ceea ce priveste self-drive-ul in cazurile masinilor care permit acest lucru.

	Proiectul a fost realizat folosind limbajul Python (versiunea 3.8). IDE-ul folosit este PyCharm iar librariile utilizate pentru procesarea imaginilor si analiza punctelor in vederea crearii unei regresii liniare cat mai exacte au fost: cv2 si numpy.

	Input-ul aplicatiei este un filmulet cu o strada, filmata de undeva de pe capota unei masini in miscare pe o strada cu dublu sens care dispune si de o banda de urgenta.

Pasii pentru realizarea aplicatiei:

-Citiesc video-ul si il pornim; Frame-ul este de fapt un numpy array unde elementele sunt de tip unsigned char;

-Micsoraez frame-ul video-ului; cu cat sunt mai multi pixeli de procesau, cu atat executia este mai lenta;

-Convertiesc imaginea la alb-negru; culorile sunt greu de procesat si o procesare defectuase poate aduce probleme in cadrul aplicatiei;

-Selectez numai strada; De obicei din acel punct din care se filmeaza, strada se afla in partea de jos in forma de trapez ocupand circa jumatate (sau mai putin) din imagine;

-Selectaez doar strada si intorc imaginea  dupa care o intindem pe toata suprafata frame-ului; Acest tip de vizualizare se cheama si birds-eye-view;

-Avand in vedere calitatea imaginii si procesarile anterioare pe imagine, pixelii tind sa dea o tenta colturoasa a benzilor de pe sosea. Din cauza aceasta voi adauga un blur pe imagine pentru ca benzile sa devina mai pline si mai soft;

-Folosind Sobel filter facem edge detection. Practic inconjor benzile albe care se afla acum in frame. Pentru a face asta folosesc o matrice care arata asa: [ [-1,-2,-1], [0,0,0], [1,2,1] ]. Am mentionat deja ca frame-ul este un numpy array. Multiplic pixelii vecini liniilor din frame cu elementrul corespunzator din matricea descrisa mai sus, si astfel se creaza o noua imagine cu benzile de pe sosea inconjurate;

-Binarizez imaginea. Transform fiecare pixel ori in absolut alb (255) ori in absolut negru (0);

-Pentru a lua coordonatele benzilor de pe sosea trebuie sa impart frame-ul in 2 pe vertical, fiecare parte de frame avand cate o banda (fiecare masina este inconjurata de 2 benzi atunci cand se afla in mers, cea care desparte sensul si cea care delimiteaza soseaua de bordura sau in cazul filmuletului meu, de banda de urgenta). Pentru a face asta trebuie sa scap de zgomot, zgomotul fiind pixeli albi ramasi in cadru dupa ce s-a binarizat imaginea, pixeli care ar putea reprezenta iarba, puncte albe pe sosea, etc. Desigur, putem scapa procentual de acest “zgomot”, insa un procent prea mare poate altera si benzile care ne intereseaza. Am folosit un procent de 10%.

-Se iau coordonatele tuturor pixelilor albi din frame. 

-Matematic vorbind, coordonatele sunt reprezentate pe o axa bidimensionala x si y. Folosind functia polyfot din libraria numpy, se face o regresie liniara pe acele puncte si se obtine o linie care traverseaza cel mai corect acele puncte din grafic.

-Se traseaza linia urmand coordonatele aflate anterior. Se face acest lucru pentru ambele jumatati de frame (ambele benzi) dupa care se combina.

-Se suprapun coordonatele liniilor peste imaginea originala si se ofera culori acestora. In cazul meu am folosit verde pentru linia care delimiteaza banda pe care se merge si banda de urgenta (deoarece acea banda poate fi depasita in anumite cazuri), si rosu pentru banda care delimiteaza sensul de mers (deoarece acea banda nu are voie sa fie calcata fara existenta unui obstacol in fata - caz care nu a fost tratat);


Pentru realizarea aplicatiei a fost nevoie de o studiere amanuntita a ce inseamna procesarea de imagini si ultizarea functiilor din libraria CV2. Pentru asta am folosit documentatia care se afla la link-ul urmator: https://opencv.org/



Bibliografie:

https://towardsdatascience.com/lane-detection-with-deep-learning-part-1-9e096f3320b7

https://www.analyticsvidhya.com/blog/2020/05/tutorial-real-time-lane-detection-opencv/

https://opencv.org/

https://numpy.org/doc/

https://www.researchgate.net/publication/274477938_Lane_Detection_Based_on_Machine_Learning_Algorithm

