# data_loader.py
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset, random_split
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from StageAwareTransformer1 import StageAwareTransformer

# =================== 数据加载函数 ===================

def load_data(batch_size=1, random_state=42):
    file_path = "teaching_quality_18weeks_with_trends_final2600.xlsx"
    data = pd.read_excel(file_path)

    # 获取每个教师的唯一 ID
    teacher_ids = data['teacher_id'].unique()

    # 创建标签列
    teacher_labels = data.groupby('teacher_id')['teaching_quality_level'].apply(lambda x: x.mode()[0]).reset_index(
        name='最终标签')
    label_encoder = LabelEncoder()
    teacher_labels['最终标签'] = label_encoder.fit_transform(teacher_labels['最终标签'])

    # 获取最终标签
    final_labels = teacher_labels['最终标签'].values

    # 创建每个教师的特征数据
    features_dict = {}
    for teacher_id in teacher_ids:
        teacher_data = data[data['teacher_id'] == teacher_id]
        teacher_data = teacher_data.sort_values(by='week')

        # 获取特征列
        feature_columns = [
            'homework_posted', 'materials_posted', 'materials_downloaded', 'homework_submitted',
            'student_questions', 'teacher_replies', 'student_total', 'student_attendance', 'students_asking',
            'low_mastery_ratio', 'student_satisfaction', 'homework_on_time',
            'materials_on_time', 'homework_graded_on_time'
        ]
        # # 教学态度
        # feature_columns = [
        #     'homework_posted', 'materials_posted',
        #     'student_questions', 'teacher_replies', 'student_total',
        #     'materials_on_time'

        # ]

        num_features = len(feature_columns)
        # 将每周的特征数据转化为嵌套列表
        teacher_weeks_data = teacher_data[feature_columns].values.tolist()
        features_dict[teacher_id] = teacher_weeks_data

    # 转换为一个列表，将每个教师的特征数据合并
    all_teacher_features = [features_dict[teacher_id] for teacher_id in teacher_ids]

    # 按照教学质量等级分层抽样（使用数值编码后的标签以避免类型不匹配）
    train_ids = []
    val_ids = []
    test_ids = []

    unique_labels = np.unique(final_labels)
    for label_int in unique_labels:  # 按类别（如优秀、良好等）进行分层抽样
        # 获取该类别下所有教师的ID
        label_teacher_ids = teacher_labels[teacher_labels['最终标签'] == label_int]['teacher_id'].values
        label_labels = final_labels[teacher_labels['teacher_id'].isin(label_teacher_ids)]

        # 分层抽样：70% 训练集，15% 验证集，15% 测试集
        train_ids_label, test_ids_label = train_test_split(
            label_teacher_ids,
            train_size=0.85,  # 85% 用于训练和验证
            stratify=label_labels,
            random_state=random_state
        )

        # 进一步将训练集分为训练集和验证集
        train_labels_label = label_labels[np.isin(label_teacher_ids, train_ids_label)]
        train_ids_label, val_ids_label = train_test_split(
            train_ids_label,
            train_size=0.8235,  # 82.35% 用于训练，17.65% 用于验证
            stratify=train_labels_label,
            random_state=random_state
        )

        train_ids.extend(train_ids_label)
        val_ids.extend(val_ids_label)
        test_ids.extend(test_ids_label)

    # 选择训练集、验证集和测试集的特征和标签
    train_features = [features_dict[teacher_id] for teacher_id in train_ids]
    val_features = [features_dict[teacher_id] for teacher_id in val_ids]
    test_features = [features_dict[teacher_id] for teacher_id in test_ids]

    train_labels = final_labels[teacher_labels['teacher_id'].isin(train_ids)]
    val_labels = final_labels[teacher_labels['teacher_id'].isin(val_ids)]
    test_labels = final_labels[teacher_labels['teacher_id'].isin(test_ids)]

    # 转换为 Tensor
    train_tensor = torch.tensor(train_features, dtype=torch.float32)
    val_tensor = torch.tensor(val_features, dtype=torch.float32)
    test_tensor = torch.tensor(test_features, dtype=torch.float32)
    train_labels_tensor = torch.tensor(train_labels, dtype=torch.long)
    val_labels_tensor = torch.tensor(val_labels, dtype=torch.long)
    test_labels_tensor = torch.tensor(test_labels, dtype=torch.long)

    # 创建数据集
    train_dataset = TensorDataset(train_tensor, train_labels_tensor)
    val_dataset = TensorDataset(val_tensor, val_labels_tensor)
    test_dataset = TensorDataset(test_tensor, test_labels_tensor)

    # 创建 DataLoader
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

    # 打印数据集的形状
    print("Train tensor shape:", train_tensor.shape)
    print("Val tensor shape:", val_tensor.shape)
    print("Test tensor shape:", test_tensor.shape)

    # 打印数据集的前几行
    print("Train tensor first 5 samples:\n", train_tensor[:5].numpy())
    print("Val tensor first 5 samples:\n", val_tensor[:5].numpy())
    print("Test tensor first 5 samples:\n", test_tensor[:5].numpy())

    return train_loader, val_loader, test_loader, num_features, len(label_encoder.classes_)


from collections import Counter

train_loader, val_loader, test_loader, input_dim, num_classes = load_data()
# 查看训练集、验证集、测试集的类别分布
for name, loader in [('Train', train_loader), ('Val', val_loader), ('Test', test_loader)]:
    all_labels = []
    for xb, yb in loader:
        all_labels.extend(yb.numpy())
    print(f"{name} Label Distribution: {dict(Counter(all_labels))}")
