
#Bu .py dosyası ile karakterleri belirlenmiş sudokuları Geri Adımlama (BackTracking) algoritması ile çözümünü buluyoruz.


# En iyi hücreyi saklama
class EntryData:
    def __init__(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n

    def set_data(self, r, c, n):
        self.row = r
        self.col = c
        self.choices = n

# Sudokuyu çözme işlem
def solve_sudoku(matrix):
    cont = [True]
    # Eğer bir çözüm doğruysa kontrolü yap
    for i in range(9):
        for j in range(9):
            if not can_be_correct(matrix, i, j): # Mümkün değilse döngden çık
                return
    sudoku_helper(matrix, cont) # Mümkünse Sudokuyu çözmeye çalış

#yardımcı Fonksiyon
def sudoku_helper(matrix, cont):
    if not cont[0]: # Stopping point 1
        return

    # Mümkün olan en iyi giriş bulma
    best_candidate = EntryData(-1, -1, 100)
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0: # Eğer dolu değilse
                num_choices = count_choices(matrix, i, j)
                if best_candidate.choices > num_choices:
                    best_candidate.set_data(i, j, num_choices)

    # Herhangi bir seçenek olmadıysa
    if best_candidate.choices == 100:
        cont[0] = False # Stopping point 1
        return

    row = best_candidate.row
    col = best_candidate.col

    # 1-9 arasındaki en iyi sonucu bul
    for j in range(1, 10):
        if not cont[0]: # Stopping point 2
            return

        matrix[row][col] = j

        if can_be_correct(matrix, row, col):
            sudoku_helper(matrix, cont)

    if not cont[0]: # Stopping point 3
        return
    matrix[row][col] = 0 # Geridönüş boş olan hücreyi işaretle
            

# kullanılmayan sayıları say
def count_choices(matrix, i, j):
    can_pick = [True,True,True,True,True,True,True,True,True,True]; # From 0 to 9 - drop 0
    
    # satırı kontrol et
    for k in range(9):
        can_pick[matrix[i][k]] = False

    # sütünu kontrol et
    for k in range(9):
        can_pick[matrix[k][j]] = False;

    # 3x3lük bölgeyi kontrol et
    r = i // 3
    c = j // 3
    for row in range(r*3, r*3+3):
        for col in range(c*3, c*3+3):
            can_pick[matrix[row][col]] = False


    count = 0
    for k in range(1, 10):  # 1 to 9
        if can_pick[k]:
            count += 1

    return count

# Eğer Geçerli gücre herhangi bir ihlal içermiyorsa True değerini döndürür
def can_be_correct(matrix, row, col):
    
    # Check row
    for c in range(9):
        if matrix[row][col] != 0 and col != c and matrix[row][col] == matrix[row][c]:
            return False

    # Check column
    for r in range(9):
        if matrix[row][col] != 0 and row != r and matrix[row][col] == matrix[r][col]:
            return False

    # Check 3x3 square
    r = row // 3
    c = col // 3
    for i in range(r*3, r*3+3):
        for j in range(c*3, c*3+3):
            if row != i and col != j and matrix[i][j] != 0 and matrix[i][j] == matrix[row][col]:
                return False
    
    return True

#Tüm bulmaca çözülmüşse True değeri döndürür
def all_board_non_zero(matrix):
    for i in range(9):
        for j in range(9):
            if matrix[i][j] == 0:
                return False
    return True