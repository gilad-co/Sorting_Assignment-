import argparse
import time
import statistics
import random
import sys
import matplotlib.pyplot as plt
# ==========================================
#sorting algorithems
# ==========================================
def bubble_sort(arr):
#protection from large arrays
    n = len(arr)
    if n > 10000:
        print(f"  [!] Skipping Bubble Sort for size {n} (Too large for O(n^2))")
        return
#start sorting
    for i in range(n):
        swapped = False

        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2  # מוצאים את האמצע
        L = arr[:mid]        # חצי שמאלי
        R = arr[mid:]        # חצי ימני

        # קריאה רקורסיבית כדי להמשיך לחתוך את החצאים
        merge_sort(L)
        merge_sort(R)

        # 2. שלב המיזוג (Merge)
        i = j = k = 0

        # משווים בין האיברים של L ו-R, ומכניסים את הקטן יותר חזרה ל-arr
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        # אם נשארו איברים רק באחד החצאים (כי השני התרוקן),
        # פשוט מכניסים את כולם ברצף לסוף המערך
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
#rapper
    _quick_sort_recursive(arr, 0, len(arr) - 1)

def _quick_sort_recursive(arr, low, high):
    if low < high:
        # pi הוא האינדקס שבו התיישב ה-Pivot אחרי החלוקה
        pi = _partition(arr, low, high)

        # קריאה רקורסיבית לחצי השמאלי ולחצי הימני (מדלגים על ה-Pivot כי הוא כבר במקום)
        _quick_sort_recursive(arr, low, pi - 1)
        _quick_sort_recursive(arr, pi + 1, high)


def _partition(arr, low, high):
    pivot_idx = random.randint(low, high)
    arr[pivot_idx], arr[high] = arr[high], arr[pivot_idx]

    pivot = arr[high]  # ה-Pivot שלנו הוא עכשיו האיבר האחרון
    i = low - 1  # i מסמן את גבול האזור של ה"קטנים מה-Pivot"

    for j in range(low, high):
        # אם מצאנו מספר שקטן מה-Pivot, אנחנו דוחפים אותו שמאלה לאזור ה"קטנים"
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    # בסוף המעבר, שמים את ה-Pivot בדיוק באמצע (אחרי כל ה"קטנים")
    arr[i + 1], arr[high] = arr[high], arr[i + 1]

    # מחזירים את המיקום הסופי של ה-Pivot
    return i + 1


# ==========================================
# חלק 2: פונקציות עזר - יצירת מערכים
# כאן נייצר את המערכים שעליהם נעשה את הניסויים
# ==========================================

def generate_random_array(size):
    return [random.randint(1, 1000000) for _ in range(size)]


def generate_nearly_sorted_array(size, noise_percentage):

    arr = list(range(1, size + 1))
#how much swaps
    num_swaps = int((noise_percentage / 100.0) * size)
#swaping
    for _ in range(num_swaps):
        idx1 = random.randint(0, size - 1)
        idx2 = random.randint(0, size - 1)
        arr[idx1], arr[idx2] = arr[idx2], arr[idx1]
    return arr

# ==========================================
# חלק 3: מדידת זמנים (ליבת הניסוי)
# ==========================================

def measure_time(algorithm_func, arr, repetitions):
#for bubble sort
    if algorithm_func.__name__ == 'bubble_sort' and len(arr) > 10000:
        return None, None

    run_times = []

    for _ in range(repetitions):

        arr_copy = arr.copy()

        start_time = time.time()

        algorithm_func(arr_copy)

        end_time = time.time()

        run_times.append(end_time - start_time)
    avg_time = statistics.mean(run_times)

    if repetitions > 1:
        std_dev = statistics.stdev(run_times)
    else:
        std_dev = 0.0

    return avg_time, std_dev


# ==========================================
# חלק 4: יצירת הגרפים (Plots)
# ==========================================

def save_plot(results_dict, filename, title):

    plt.figure(figsize=(10, 6))

    for algo_name, data in results_dict.items():
        sizes = data['sizes']
        avgs = data['avgs']
        stds = data['stds']

        line = plt.plot(sizes, avgs, marker='o', label=algo_name)[0]

        lower_bound = [max(0, a - s) for a, s in zip(avgs, stds)]
        upper_bound = [a + s for a, s in zip(avgs, stds)]

     #סטיית תקן
        plt.fill_between(sizes, lower_bound, upper_bound, alpha=0.2, color=line.get_color())

    # הוספת כל הכיתובים מסביב לפי ההנחיות במסמך
    plt.title(title)
    plt.xlabel("Array size (n)")
    plt.ylabel("Runtime (seconds)")

    plt.legend()


    plt.grid(True, linestyle='--', alpha=0.7)

    plt.savefig(filename)
    plt.close()


# ==========================================
# חלק 5: הפונקציה הראשית (Main) - סעיף ד' בעבודה
# ==========================================

def main():
    # 1. הגדרת הארגומנטים לשורת הפקודה לפי ההנחיות
    parser = argparse.ArgumentParser(description="Sorting Algorithms Experiments")
    parser.add_argument('-a', '--algorithms', type=int, nargs='+', required=True,
                        help="1-Bubble, 2-Selection, 3-Insertion, 4-Merge, 5-Quick")
    parser.add_argument('-s', '--sizes', type=int, nargs='+', required=True,
                        help="Array sizes (e.g., 100 500 1000)")
    parser.add_argument('-e', '--experiment', type=int, choices=[0, 1, 2], required=True,
                        help="0-Random (Part B), 1-Nearly sorted 5% (Part C), 2-Nearly sorted 20%")
    parser.add_argument('-r', '--repetitions', type=int, default=1,
                        help="Number of repetitions")

    args = parser.parse_args()

    # מילון שמתרגם את המספר שהמשתמש הקליד (1, 4 או 5) לפונקציה האמיתית שכתבנו
    # (מכיוון שבחרנו לא לממש את 2 ו-3, לא הכנסנו אותם לכאן)
    available_algos = {
        1: bubble_sort,
        4: merge_sort,
        5: quick_sort
    }

    # מילון לאיסוף כל התוצאות לטובת הגרף בסוף
    results_dict = {}

    print(f"Starting experiments with {args.repetitions} repetitions per size...")

    # 2. הלולאה הראשית - עוברת על כל מספר אלגוריתם שהמשתמש ביקש
    for algo_id in args.algorithms:
        if algo_id not in available_algos:
            print(f"Algorithm ID {algo_id} is not implemented. Skipping.")
            continue

        algo_func = available_algos[algo_id]
        algo_name = algo_func.__name__.replace('_', ' ').title()

        print(f"--- Running {algo_name} ---")

        avgs = []
        stds = []
        valid_sizes = []  # נשמור רק גדלים שהאלגוריתם באמת הצליח לרוץ עליהם (בגלל ההגנה על הבועות)

        # 3. הלולאה הפנימית - עוברת על כל גודל מערך שהמשתמש ביקש
        for size in args.sizes:
            # מחליטים איזה מערך לייצר לפי סוג הניסוי (-e)
            if args.experiment == 0:
                arr = generate_random_array(size)
                title = "Runtime Comparison (Random Arrays)"
                filename = "result1.png"
            elif args.experiment == 1:
                arr = generate_nearly_sorted_array(size, noise_percentage=5)
                title = "Runtime Comparison (Nearly Sorted, noise=5%)"
                filename = "result2_5percent.png"
            elif args.experiment == 2:
                arr = generate_nearly_sorted_array(size, noise_percentage=20)
                title = "Runtime Comparison (Nearly Sorted, noise=20%)"
                filename = "result2_20percent.png"

            # מודדים זמן! קוראים לחלק 3
            avg_time, std_time = measure_time(algo_func, arr, args.repetitions)

            # אם קיבלנו זמן (כלומר זו לא הייתה ריצה שחסמנו בכוונה כמו בועות ענק)
            if avg_time is not None:
                avgs.append(avg_time)
                stds.append(std_time)
                valid_sizes.append(size)
                print(f"  Size {size}: Avg = {avg_time:.4f}s, StdDev = {std_time:.4f}s")

        # שומרים את כל הרשימות האלו במילון תחת השם של האלגוריתם
        results_dict[algo_name] = {'sizes': valid_sizes, 'avgs': avgs, 'stds': stds}

    # 4. מציירים את הגרף! קוראים לחלק 4
    if results_dict:
        print(f"\nSaving plot to {filename}...")
        save_plot(results_dict, filename, title)
        print("Done!")


# הפקודה שמתניעה את כל הקובץ
if __name__ == "__main__":
    main()