import pandas as pd
import numpy as np
import random

# 标签对应的 δ（延迟发布频率）均值与标准差
delta_values = {
    '0': (0.05, 0.01),
    '1': (0.10, 0.02),
    '2': (0.20, 0.03),
    '3': (0.35, 0.05)
}

# 标签对应的 m（教师可用时间系数）均值与标准差
time_available_values = {
    '0': (0.9, 0.03),
    '1': (0.75, 0.05),
    '2': (0.6, 0.07),
    '3': (0.45, 0.08)
}

# 生成作业难度系数 k（每周变化）
def generate_difficulty():
    return np.clip(np.random.normal(0.5, 0.1), 0.1, 0.9)

# 给定标签，扰动生成 δ 和 m
def get_delta_and_time_available(label):
    delta_mu, delta_sigma = delta_values[label]
    m_mu, m_sigma = time_available_values[label]
    delta = np.clip(np.random.normal(delta_mu, delta_sigma), 0, 1)
    m = np.clip(np.random.normal(m_mu, m_sigma), 0, 1)
    return delta, m

# 根据公式 Bt = At − δ(1+k)(1−m) 计算按时发布作业数量
def calculate_on_time_homework(A_t, label):
    delta, m = get_delta_and_time_available(label)
    k = generate_difficulty()  # 难度系数
    B_t = A_t - delta * (1 + k) * (1 - m)
    return max(0, min(A_t, B_t))  # 保证 B_t 不小于0也不超过 A_t

#(3)按时发布的资料数量（D）
# 定义标签对应的不按时发布的比率ϵ
epsilon_values = {
    '0': 0.05,   # 假设优秀的按时发布比例较高，5%的资料不按时发布
    '1': 0.1,    # 良好的按时发布比例适中，10%的资料不按时发布
    '2': 0.2,    # 合格的按时发布比例较低，20%的资料不按时发布
    '3': 0.3   # 不合格的按时发布比例最差，30%的资料不按时发布
}

# 扰动方法，确保扰动值不会为负数
def apply_epsilon_disturbance(epsilon, std_dev, max_disturb_ratio=0.1):
    """
    对ϵ值进行扰动，确保结果不为负数。
    epsilon: 当前的ϵ值
    std_dev: 扰动的标准差
    max_disturb_ratio: 最大扰动比例（相对于原始ϵ值）
    """
    # 正态分布扰动
    disturbance = np.random.normal(0, std_dev)
    disturbance = epsilon * (disturbance / epsilon)  # 正常化扰动
    disturbance = max(-epsilon * max_disturb_ratio, min(disturbance, epsilon * max_disturb_ratio))

    # 扰动后的ϵ值
    disturbed_epsilon = epsilon + disturbance

    # 确保不为负数
    return max(0, disturbed_epsilon)

# 计算按时发布的资料数量Dt
def calculate_on_time_materials(Ct, label, std_dev=0.02, max_disturb_ratio=0.1):
    """
    根据标签和发布的资料数量计算按时发布的资料数量。
    Ct: 发布的资料数量
    label: 教学标签（如优秀、良好等）
    """
    epsilon = epsilon_values[label]  # 获取对应标签的不按时发布的比率ϵ
    # 对ϵ值进行扰动
    disturbed_epsilon = apply_epsilon_disturbance(epsilon, std_dev, max_disturb_ratio)
    Dt = Ct * (1 - disturbed_epsilon)  # 按时发布的资料数量
    return Dt

#(4)下载的资料数量（E）
# 定义标签对应的α值
alpha_values = {
    '0': 0.1,  # 假设优秀的衰减因子α较小
    '1': 0.2,  # 良好的衰减因子α适中
    '2': 0.3,  # 合格的衰减因子α较大
    '3': 0.4  # 不合格的衰减因子α最大
}

# 对α值进行扰动，并保证其不为负
def apply_alpha_disturbance(alpha, std_dev=0.05, max_disturb_ratio=0.2):
    """
    对α值进行扰动，确保结果不为负数。
    alpha: 当前的α值
    std_dev: 扰动的标准差
    max_disturb_ratio: 最大扰动比例（相对于原始α值）
    """
    # 正态分布扰动
    disturbance = np.random.normal(0, std_dev)
    disturbance = alpha * (disturbance / alpha)  # 正常化扰动
    disturbance = max(-alpha * max_disturb_ratio, min(disturbance, alpha * max_disturb_ratio))

    # 扰动后的α值
    disturbed_alpha = alpha + disturbance

    # 确保不为负数
    return max(0, disturbed_alpha)


# 更新下载量衰减因子的计算
def calculate_downloaded_materials(Ct, Dt, S, label, std_dev=0.05, max_disturb_ratio=0.2):
    """
    计算下载量，使用扰动后的α值。
    """
    alpha = alpha_values[label]  # 获取标签对应的α值
    # 对α值进行扰动
    disturbed_alpha = apply_alpha_disturbance(alpha, std_dev, max_disturb_ratio)
    download_factor = 1 - disturbed_alpha * (Ct - Dt)  # 计算下载量衰减因子
    Et = Ct * S * download_factor  # 计算下载量
    return Et

#(5)提交的作业数量（F）
# 定义标签对应的参数：最低提交率γ，作业难度系数k
parameters = {
    '0': {'γ': 0.9},  # 优秀学生的作业提交率高，作业难度低
    '1': {'γ': 0.8},  # 良好学生的作业提交率适中，作业难度中等
    '2': {'γ': 0.7},  # 合格学生的作业提交率较低，作业难度较高
    '3': {'γ': 0.6}  # 不合格学生的作业提交率最低，作业最难
}


# 扰动函数
def add_disturbance(value, std_dev, min_val=0, max_val=1):
    """
    对给定的值进行扰动，确保扰动后的值在[min_val, max_val]之间。
    value: 基准值
    std_dev: 标准差，控制扰动幅度
    min_val: 最小值
    max_val: 最大值
    """
    disturbance = np.random.normal(0, std_dev)  # 正态分布扰动
    new_value = value + disturbance

    # 限制新值在[min_val, max_val]之间
    return max(min_val, min(new_value, max_val))


# 计算学生兴趣度n的函数
def calculate_n(k, alpha=0.5, beta=0.3):
    """
    根据作业难度系数k计算学生兴趣度系数n。
    k: 作业难度系数
    alpha: 作业难度与学生兴趣度之间的关系强度
    beta: 学生兴趣度的最小值
    """
    n = alpha * (1 - k) + beta
    return n


# 计算g(D)函数
def calculate_gd(Dt, γ, k, n, Ct):
    """
    根据按时发布的资料数量D计算g(D)。
    D: 按时发布的资料数量
    γ: 最低提交率
    k: 作业难度系数
    n: 学生兴趣度系数
    C: 总的学生人数
    """
    if Ct==0:
        return γ
    g_D=γ + (1 - γ) * (Dt * (1 - k) * n) / Ct
    return g_D


def calculate_F(Dt, Ct, At, S, label, std_dev=0.05, max_disturb_ratio=0.2):
    """
    计算提交的作业数量F。
    """
    k = generate_difficulty()  # 难度系数
    gamma = parameters[label]['γ']
    n = calculate_n(k)
    g_D = calculate_gd(Dt, gamma, k, n, Ct)
    if np.isnan(g_D):
        g_D = gamma
    Ft = g_D * At * S
    return Ft

#(6)按时批改的作业数量（G）
# 定义标签对应的教师批改效率系数q和批改衰减系数λ
teacher_parameters = {
    '0': {'q': 0.9, 'λ': 0.2,},  # 优秀教师批改效率高，衰减系数较低
    '1': {'q': 0.75, 'λ': 0.3},  # 良好教师批改效率适中，衰减系数适中
    '2': {'q': 0.6, 'λ': 0.4},  # 合格教师批改效率较低，衰减系数较高
    '3': {'q': 0.5, 'λ': 0.5}  # 不合格教师批改效率最低，衰减系数最高
}


# 扰动函数
def add_disturbance(value, std_dev, min_val=0, max_val=1):
    """
    对给定的值进行扰动，确保扰动后的值在[min_val, max_val]之间。
    value: 基准值
    std_dev: 标准差，控制扰动幅度
    min_val: 最小值
    max_val: 最大值
    """
    disturbance = np.random.normal(0, std_dev)  # 正态分布扰动
    new_value = value + disturbance

    # 限制新值在[min_val, max_val]之间
    return max(min_val, min(new_value, max_val))


# 计算教师批改作业数量Gt的函数
def calculate_G(Ft, At, label):
    """
    计算教师批改作业数量Gt
    Ft: 提交的作业数量
    λ: 批改衰减系数
    At: 发布的作业数量
    q: 教师批改效率系数
    k: 作业难度系数
    """
    q = teacher_parameters[label]['q']
    λ = teacher_parameters[label]['λ']
    k = generate_difficulty()  # 难度系数

    q_std_dev = 0.1  # 批改效率系数扰动的标准差
    lambda_std_dev = 0.1  # 批改衰减系数扰动的标准差
    k_std_dev = 0.1

    # 对q和λ进行扰动
    disturbed_q = add_disturbance(q, q_std_dev)
    disturbed_λ = add_disturbance(λ, lambda_std_dev)
    disturbed_k = add_disturbance(k, k_std_dev)

    Gt = Ft - disturbed_λ * At * (1 - disturbed_q) * disturbed_k
    return Gt





# 设置随机种子
np.random.seed(42)
random.seed(42)

# 标签定义和每类教师数量
labels = ['0', '1', '2', '3']
#teachers_per_label = 1000  # 每个标签位教师

teachers_per_label = {
    '0': 413,  # 优秀教师
    '1': 887,   # 良好教师
    '2': 887,   # 合格教师
    '3': 413
        # 不合格教师
}

weeks_per_teacher = 18  # 每位教师18周

# 定义每个标签下的字段分布（均值, 标准差）
distributions = {
    '0': {
        'homework_posted': (4, 1), 'homework_on_time': (4, 1),
        'materials_posted': (6, 1.5),
        'student_questions': (15, 5), 'teacher_replies': (15, 5),
        'low_mastery_ratio': (0.05, 0.03), 'student_satisfaction': (90, 5)
    },
    '1': {
        'homework_posted': (3, 1), 'homework_on_time': (3, 1),
        'materials_posted': (5, 2),
        'student_questions': (10, 4), 'teacher_replies': (10, 4),
        'low_mastery_ratio': (0.10, 0.05), 'student_satisfaction': (80, 7)
    },
    '2': {
        'homework_posted': (2, 1), 'homework_on_time': (2, 1),
        'materials_posted': (4, 2),
        'student_questions': (6, 3), 'teacher_replies': (6, 3),
        'low_mastery_ratio': (0.15, 0.08), 'student_satisfaction': (70, 10)
    },
    '3': {
        'homework_posted': (1, 1), 'homework_on_time': (1, 1),
        'materials_posted': (2, 1),
        'student_questions': (3, 2), 'teacher_replies': (3, 2),
        'low_mastery_ratio': (0.3, 0.1), 'student_satisfaction': (50, 15)
    }
}

# 初始化数据列表
data = []
teacher_id = 1

for label in labels:
    for _ in range(teachers_per_label[label]):
        student_total = np.random.randint(30, 61)
        for week in range(1, weeks_per_teacher + 1):
            d = distributions[label]
            week_norm = week / weeks_per_teacher

            attend_ratio = 1 - 0.15 * week_norm + np.random.normal(0, 0.03)
            student_attendance = max(0, min(student_total, int(student_total * attend_ratio)))

            ask_ratio = 0.5 + 0.3 * np.sin(week_norm * np.pi) + np.random.normal(0, 0.05)
            students_asking = max(0, min(student_attendance, int(student_attendance * ask_ratio)))

            homework_posted=max(0, int(np.random.normal(*d['homework_posted'])) + int(week_norm * 1.5))
            materials_posted=max(0, int(np.random.normal(*d['materials_posted'])))
            materials_on_time = int(calculate_on_time_materials(materials_posted, label))
            materials_downloaded = int(calculate_downloaded_materials(materials_posted, materials_on_time, student_total, label))
            alpha = alpha_values[label]  # 获取标签对应的α值
            # 对α值进行扰动
            disturbed_alpha = apply_alpha_disturbance(alpha)
            print(f"week:{week},Ct: {materials_posted}, Dt: {materials_on_time}, S: {student_total}, label: {label}, alpha: {alpha}, disturbed_alpha: {disturbed_alpha},Et: { materials_downloaded}")
            homework_submitted = int(calculate_F(materials_on_time, materials_posted,  homework_posted, student_total, label))
            homework_graded_on_time = int(calculate_G(homework_submitted,  homework_posted, label))

            if label == '0':
                satisfaction = d['student_satisfaction'][0] + 5 * week_norm + np.random.normal(0, d['student_satisfaction'][1])
            else:
                satisfaction = d['student_satisfaction'][0] - 5 * week_norm + np.random.normal(0, d['student_satisfaction'][1])
            satisfaction = min(max(0, satisfaction), 100)

            if label in ['2', '3']:
                mastery_ratio = d['low_mastery_ratio'][0] + 0.05 * week_norm + np.random.normal(0, d['low_mastery_ratio'][1])
            else:
                mastery_ratio = d['low_mastery_ratio'][0] + np.random.normal(0, d['low_mastery_ratio'][1])
            mastery_ratio = min(max(0, mastery_ratio), 1.0)

            record = {
                'teacher_id': f"T{teacher_id:03d}",
                'week': week,
                'homework_posted':  homework_posted,
                'materials_posted': materials_posted,
                'materials_downloaded': materials_downloaded,  # 更新
                'homework_submitted': homework_submitted,  # 更新
                'student_questions': max(0, int(np.random.normal(*d['student_questions']))),
                'teacher_replies': max(0, int(np.random.normal(*d['teacher_replies']))),
                'student_total': student_total,
                'student_attendance': student_attendance,
                'students_asking': students_asking,
                'low_mastery_ratio': mastery_ratio,
                'student_satisfaction': satisfaction,
                'teaching_quality_level': label
            }
            record['homework_on_time'] = min(record['homework_posted'], int(np.random.normal(*d['homework_on_time'])))
            record['materials_on_time'] = int(min(record['materials_posted'], materials_on_time))
            record['homework_graded_on_time'] = min(record['homework_submitted'], homework_graded_on_time)
            data.append(record)
        teacher_id += 1

# 注入“优秀”中的噪声
excellent_teachers = {r['teacher_id'] for r in data if r['teaching_quality_level'] == '0'}
noisy_teachers = random.sample(list(excellent_teachers), 2)
for record in data:
    if record['teacher_id'] in noisy_teachers and record['week'] in [5, 10, 15]:
        record['low_mastery_ratio'] = min(max(0.25 + np.random.rand() * 0.2, 0), 1)
        record['student_satisfaction'] = max(50, record['student_satisfaction'] - np.random.rand() * 50)

# 导出为 Excel
df = pd.DataFrame(data)
file_path = "teaching_quality_18weeks_with_trends_final2600.xlsx"
df.to_excel(file_path, index=False)
file_path
