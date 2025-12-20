translate turkish strings:

    # game/code/minigames/nonogram/nonogram_tutorial.rpy:48
    old "Your goal in these puzzles is to fill the whole grid with green and black squares.\n\nAbove and to the left of the grid are numbers. These are the indicator numbers that tell you the number of green squares in that specific row and column.\n\nExample. If the row has a '3' next to it, that means there will be a set of three green (connected) squares somewhere in that row. It is the same for columns based on the numbers at the top of the puzzle. A '2' at the top of a column means that in that column, there is a set of two green squares running vertically."
    new "Amacınız ızgarayı yeşil ve siyah karelerle doldurmaktır.\n\nIzgaranın üstünde ve solundaki sayılar, o satır/sütundaki yeşil karelerin sayısını gösterir.\n\nÖrnek: Bir satırda '3' varsa, o satırda üç bağlı yeşil kare vardır. Üstteki '2', o sütunda dikey iki yeşil kare olduğunu belirtir."

    # game/code/minigames/nonogram/nonogram_tutorial.rpy:53
    old "You will notice some rows/columns have 2 numbers.\n\nIf you see '2 1', that tells you that somewhere in that line will be a run of exactly 2 green squares, followed by 1 or more black squares, followed by 1 green square.\n\nThere might be black squares before or after the green squares - only the runs of green squares are counted."
    new "Bazı satır/sütunlarda iki sayı görürsünüz.\n\n'2 1' demek: önce tam 2 yeşil, sonra 1+ siyah, sonra 1 yeşil.\n\nSiyahlar başta/sonda olabilir; sadece yeşil diziler sayılır."

    # game/code/minigames/nonogram/nonogram_tutorial.rpy:58
    old "Left-click on a square to make it green. Right-click to mark with black.\n\nIn our system, the black squares represent the empty or blank squares and the green squares are the coded or filled squares.\n\nYou do not need to fill in the blank squares by marking them if you do not want to. It is not required to solve the puzzle."
    new "Bir kareyi yeşile çevirmek için sol, siyahla işaretlemek için sağ tıklayın.\n\nSiyah kareler boşu, yeşiller doluyu temsil eder.\n\nBoş kareleri işaretlemek şart değildir; bulmaca onsuz da çözülebilir."

    # game/code/minigames/nonogram/nonogram_tutorial.rpy:63
    old "It is strongly advised never to guess. Only squares that can be determined by logic should be coded or filled green.\n\nIt is easy for a single error to cause inaccuracies across the entire puzzle.\n\nSimple puzzles can usually be solved by figuring out the reasoning by focusing on a single row/column at a time. Then move to the next row and the next row until you have filled all the green squares."
    new "Rastgele tahmin etmeyin; yalnızca mantıkla belirlenebilen kareleri yeşil yapın.\n\nTek bir hata tüm bulmacayı bozabilir.\n\nBasit bulmacalarda tek tek satır/sütunlara odaklanın ve yeşilleri doldurarak sırayla ilerleyin."

    # game/code/minigames/nonogram/nonogram_tutorial.rpy:68
    old "Some more challenging puzzles may also require several types of reasoning that include more than one row (or column).\n\nYou might think that you have the correct answer for one row, but your answer might not work for an intersecting column. Resolving these contradictions is key to solving more complicated puzzles.\n\nWhen a cell cannot be a coded/green square because some other cell would produce an error, it should be a black/blank square - and vice versa.\n\nWhen you are confident in your solution, click the checkmark to submit the program for code review."
    new "Daha zorlu bulmacalar, birden çok satır/sütunu birlikte düşünmeyi gerektirir.\n\nBir satırdaki çözüm, kesişen bir sütunla çelişebilir; bu çelişkileri giderin.\n\nBir hücre yeşil olamazsa siyah olmalıdır — ve tersi.\n\nÇözümünüzden emin olduğunuzda, onay işaretine tıklayıp kod incelemesine gönderin."

