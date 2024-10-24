import random
def middle_rectangles(x1, x2, N, func, x):
    # Розрахунок ширини кожного прямокутника
    delta_x = (x2 - x1) / N
    
    # Ініціалізація змінної для зберігання суми площ
    area = 0
    
    # Цикл по кожному розбиттю
    for i in range(N):
        # Знаходимо середину кожного прямокутника
        midpoint = x1 + (i + 0.5) * delta_x
        
        # Обчислюємо значення функції в точці середини
        f_value = func.subs(x, midpoint)
        
        # Додаємо площу прямокутника до загальної площі
        area += f_value * delta_x
    
    return area

def trapezoidal(x1, x2, N, func, x):
    # Розрахунок ширини кожного інтервалу
    delta_x = (x2 - x1) / N
    
    # Обчислюємо значення функції в кінцевих точках
    area = (func.subs(x, x1) + func.subs(x, x2)) / 2
    
    # Додаємо значення функції в проміжних точках
    for i in range(1, N):
        xi = x1 + i * delta_x
        area += func.subs(x, xi)
    
    # Множимо на ширину інтервалу для отримання кінцевого результату
    area *= delta_x
    
    return area

def monte_carlo(x1, x2, N, func, x):
    # Генеруємо випадкові точки в межах [x1, x2]
    total_area = 0
    
    for _ in range(N):
        # Випадкова точка по осі x
        random_x = random.uniform(x1, x2)
        
        # Значення функції в точці random_x
        f_value = func.subs(x, random_x)
        
        # Додаємо до загальної суми
        total_area += f_value
    
    # Обчислюємо середнє значення і множимо на (x2 - x1)
    area = (x2 - x1) * (total_area / N)
    
    return area
