#A merge sort algorithm for sorting  a 2d array by the second elements
def merge_sort(array):  # 4 usages
    if len(array) > 1:
        mid = len(array) // 2
        array1 = array[:mid]
        array2 = array[mid:]
        merge_sort(array1)
        merge_sort(array2)

        i, j, k = 0, 0, 0

        while i < len(array1) and j < len(array2):
            if array1[i][1] > array2[j][1]:
                array[k] = array1[i]
                i += 1
            else:
                array[k] = array2[j]
                j += 1
            k += 1

        while i < len(array1):
            array[k] = array1[i]
            i += 1
            k += 1

        while j < len(array2):
            array[k] = array2[j]
            j += 1
            k += 1
scores = ["Finn-200","Bulcsu-150","Huey-201","Will-0"]

#function to update the scores
def update_scores(score_list):
    scoreFile = open("scores.txt","r")
    currentScore = "X"

    #create an array of scores
    while currentScore != "":
        currentScore = scoreFile.readline()
        currentScore = currentScore.strip()
        if currentScore != "":
            score_list.append(currentScore)

    #prepare the list for a merge sort
    for i in range(len(score_list)):
        score_list[i] = score_list[i].split("-")
        score_list[i][1] = int(score_list[i][1])
    merge_sort(score_list)
    scoreFile.close()
    scoreFile = open("scores.txt","w")

    #update the file
    for i in range(len(score_list)):
        scoreFile.write(score_list[i][0]+"-"+str(score_list[i][1])+"\n")
    scoreFile.close()