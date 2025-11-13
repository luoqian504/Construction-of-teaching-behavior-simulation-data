# Construction-of-teaching-behavior-simulation-data
为了系统地评估模型捕捉具有教学意义的时间模式的能力，我们基于领域知识生成规则构建了一个行为结构化的合成数据集。这种设计可以完全控制每周行为之间的因果关系，并确保在模型解释中的可追溯性。 虽然最终目标是从现实世界的教学数据中得出可操作的见解，但本研究采用基于模拟的设计，严格评估基于Transformer的架构是否能够有效地从结构化、随时间演变的教学行为中学习。模拟环境作为一个受控的测试平台，用于验证模型识别行为模式并进行准确教师类型分类的能力，从而为后续应用于现实世界数据集和探索性教育分析奠定可靠的基础。

（1）仿真规则的来源说明

 为确保仿真数据具备教育场景的合理性与实际教学行为的一致性，本研究在构建仿真规则体系时，综合参考了真实平台教学数据特征、教学行为理论与指标体系、专家意见与迭代试验。
 首先以“头歌实践教学平台”为数据场景蓝本，参考其课程运行过程中的教学行为记录项，例如，任务完成进度、课堂互动、作业提交反馈、评分情况等。虽未直接调用真实数据，但仿真规则在数据分布、指标类型及演化逻辑上严格模仿其多维度、周期性特征。其次，参考了高校课堂教学质量评价常用的分阶段指标体系，如“教学准备”、“任务落实”、“课堂反馈”、“教学互动”和“教学满意度”等，结合 Bloom 教学目标分类理论，从认知、技能和态度层面建立行为映射。同时，在规则设定初期，邀请了3位具备一线教学经验的高校教师参与讨论，对规则中关键权重项（如行为偏移、评价权重）进行了多轮调参与修正，确保逻辑链的可解释性与符合教育实际。

（2）教师类型建模 

	为模拟不同类型教师在教学过程中的行为差异，本文将教师划分为四个等级：优秀（Level0）、良好（Level1）、合格（Level2）和不合格（Level3）。
	每一等级在教学投入、任务管理及资源发布等方面存在显著差异，这些差异通过一组参数化的行为特征加以体现。参数的设计综合参考了教学管理理论与平台实证数据的启发，旨在生成具有区分度的教学行为序列。具体而言，不同参数控制了教师在作业布置、资源发布、学生互动及批改环节中的行为表现，形成了教学质量差异的基础。
	作业延迟频率（δ）：反映教师在作业布置环节的时间管理能力。优秀教师几乎不出现延迟，而不合格教师延迟频率较高。
	可用时间系数（m）：表示教师在学期内投入教学活动的相对时间比例。优秀教师时间充裕与，不合格教师时间有限。
	资源延迟发布比率(ϵ)：刻画教师在教学资源发布方面的及时性，值越大表示发布越滞后。
	最低提交率(γ)：反映教师课堂管理与学生激励效果，决定了学生按时提交作业的最低比例。
	批改效率系数(q)与批改衰减系数(α)：共同描述教师在批改任务中的效率与随时间的衰减趋势。高水平教师批改及时、衰减慢；低水平教师效率低、衰减显著。
	资源下载衰减系数(α)：表示教学资源被学生持续访问的下降速度，间接反映教师教学资源的吸引力。
	作业难度水平（k）：控制作业设计的复杂度，取值范围[0.1,0.9]，可用于模拟不同课程类型或阶段的教学任务。
	各教师类型的具体参数设置如表2所示。其中，参数为正态分布时以N（μ，σ）表示。
 
表2 教师类型相关参数

<img width="1373" height="361" alt="image" src="https://github.com/user-attachments/assets/45a653cb-d20c-4316-8677-78dc8156b006" />

（3）每周指标生成规则 

在18周的模拟中，每周t都会为每位教师生成一组结构化的行为特征，对于作业发布数量（ <img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/8e242e5f-8968-44ca-84ac-f7b3989f40b0" />
）、发布的资料数量（<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/ca703a7a-2605-4853-8746-866653b91288" />
 ）、学生提问的数量（<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/0df927db-c7b4-42f4-a65f-8b6d7ebc6d32" />
 ）、教师回复的数量（<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/abf54937-1be5-4a5c-9ede-0eea45ac9817" />
 ）、总的学生人数S等指标，按不同教师类型采用正态分布的方式生成，其余指标计算方式如下：
 
按时发布的作业数量<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/04efd58d-9443-42f0-8494-01cbcb908961" />
 使用公式（18）计算。

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/efa27c8b-4f7f-4da3-99c8-ae96d5fc2d29" />,	(18)

按时发布的资料数量<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/ca234ef1-e6ac-48be-baee-cd7e3e96ea4b" />
使用公式（19）计算。

<img width="90" height="22" alt="image" src="https://github.com/user-attachments/assets/35bd88eb-dcf0-45aa-a0e5-22684a7e4d9c" />,	(19)

下载的资料数量<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/9e40c283-2ab9-45d9-9872-71e612ddd3e0" />
使用公式（20）（21）计算。

<img width="120" height="30" alt="image" src="https://github.com/user-attachments/assets/cecef2e8-6cc5-4b35-9972-fc5ab5cdbc81" />,	(20)

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/aaddb6c3-8995-45a8-ad13-b0572a070d5b" />,(21)

其中，  <img width="45" height="25" alt="image" src="https://github.com/user-attachments/assets/8ec1ba19-12b5-4960-b625-c76f95b9b1ee" />
为下载量衰减因子。 


提交的作业数量<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/3abd6954-9d91-4dbf-8037-a5d26f4b0f02" />
使用公式（22）（23）（24）计算。

<img width="110" height="25" alt="image" src="https://github.com/user-attachments/assets/17ae0a10-855f-4307-a8f8-02a6d571367e" />,	(22)

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/cd046bb6-addb-4665-b8df-290faaf35838" />, (23)

<img width="70" height="20" alt="image" src="https://github.com/user-attachments/assets/a5b0a5eb-529d-46a7-a710-3e9122bde39c" />, (24) 

其中，  <img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/53c0fd6b-c25c-410f-ac97-2b84784570d8" />
受按时发布的资料影响，n（0<n<1）为学生对课程的兴趣度系数。 


按时批改的作业数量<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/19e0244e-17a1-427b-b00f-df44cf379254" />
使用公式（25）计算。

<img width="110" height="35" alt="image" src="https://github.com/user-attachments/assets/c5c0e8ea-2498-4e1b-9d85-005956bb3a19" />.	(25)

出勤的学生人数<img width="15" height="20" alt="image" src="https://github.com/user-attachments/assets/2720d281-e586-48c9-9f98-bacdfbb68b7a" />
使用公式（26）（27）计算。

<img width="120" height="35" alt="image" src="https://github.com/user-attachments/assets/3ec61c3b-d769-465e-8557-bf4c5fd4336d" />,	(26)

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/7075cc14-39c7-41fb-9ac1-c9bab773a707" />,	(27)

其中，ϵ1∼N(0,0.03)，  <img width="13" height="20" alt="image" src="https://github.com/user-attachments/assets/1d8dc953-d3ea-44a5-8402-96d4ff369d6a" />
为第t周的出勤率。t/T表示对教学周次进行归一化（如第9周/18周 = 0.5），用于后续模拟数据中的时间趋势。


提问的学生人数<img width="18" height="20" alt="image" src="https://github.com/user-attachments/assets/71f34932-f201-499d-8c74-f31e8c296718" />
使用公式（28）（29）计算。

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/c58471b1-7733-47da-b160-812bad51adf9" /> ,	(28)

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/628e42bb-8fa1-45e2-a040-61cffd48e185" />.	(29)

提问率呈现周期性变化，中间（如第9周）达到高峰，前后低，模拟学生提问活跃度的变化。其中，ϵ2∼N(0,0.05)，ASKt为第t周的提问率。


掌握情况未达标的学生比例<img width="18" height="20" alt="image" src="https://github.com/user-attachments/assets/388ac397-ec44-4847-a050-320407ce3736" />
使用公式（30）计算。

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/5a26d88c-f90e-4d38-b8d9-cb317cd41d9a" />,	(30)

其中，μ为该教师类型正态分布生成初始掌握情况未达标的学生数的均值，ϵ3∼N(0,σ)，σ为该教师类型生成初始掌握情况未达标的学生数的标准差。“合格/不合格”教师的掌握未达标率随着时间上升，“优秀/良好”教师的该比例稳定，仅有轻微波动，反映教师教学成效随时间的不同表现。


学生满意度<img width="18" height="20" alt="image" src="https://github.com/user-attachments/assets/2139c9f5-bec9-4766-b5c8-0aa0caedbc85" />
使用公式（31）计算。

<img width="150" height="35" alt="image" src="https://github.com/user-attachments/assets/1560e756-83e7-43a5-a14d-322d8095c02a" />，	(31)

其中，μ为该教师类型正态分布生成的学生满意度的均值，ϵ4∼N(0,σ)，σ为该教师类型正态分布生成的学生满意度的标准差。“优秀”教师的满意度随时间上升，其他标签教师的满意度随时间下降，模拟了教师教学效果和学生体验感知的时间演化差异。

