# from ..general import Field, Struct, DataSample, Util, ClassDomain, Label
# from tqdm import tqdm
# from .base_parse import BaseParse
# from ..io import FileIO
# from collections import defaultdict
#
#
# class KeyPoint2DParse(BaseParse):
#
#     def parse_class_domain(self):
#
#         label_domain_info = dict()  # {task_uid: class_domain}
#         keypoint_domain_info = defaultdict(dict)  # {task_uid: {category_id: class_domain}}
#         raw_task_info = defaultdict(dict)  # {task_uid: {category_id: category_info_dic}}
#         parent_class_domain = ClassDomain(FileIO.clean(f"{self._dataset_name}{self.PARENT_PATTERN}ClassDom"))
#         for task in tqdm(self._data_info["tasks"], desc="parsing class domain..."):
#             task_name, task_type, task_source, catalog = task['name'], task["type"], task['source'], task["catalog"]
#             task_uid = f"{task_type}${task_name}${task_source}"
#             if task_type not in (self.KEYPOINT2D_ANN_TYPE, self.DETECTION_ANN_TYPE, self.INSTANCE_SEG_ANN_TYPE):
#                 # keypoint 任务内只考虑 keypoint2d, box2d, polygon三种标注内容
#                 continue
#             # this_class_domain只用来保存当前task表示的domain
#             this_class_domain = ClassDomain(self.parse_domain_name(task_type)[0])
#             label_domain_info[task_uid] = this_class_domain
#             for category_info in catalog:
#                 category_id, category_name = category_info["category_id"], category_info["category_name"]
#                 raw_task_info[task_uid][category_id] = category_info
#                 supercategories = category_info.get("supercategories", [])
#                 this_label = Label(category_name)
#                 this_class_domain.add_label(this_label, ori_id=category_id)
#
#                 for super_cat in supercategories:
#                     super_label = Label(super_cat)
#                     parent_class_domain.add_label(super_label)
#                     this_label.add_supercategory(super_label)
#                     this_class_domain.set_parent(parent_class_domain)
#
#                 if category_info.get("point_names") and category_info.get("skeleton"):
#                     # 如果是keypoint任务
#                     points_names, skeleton = category_info["point_names"], category_info["skeleton"]
#                     domain_name = f"KeyPoint_{category_name}_ClassDom"
#                     this_point_domain = ClassDomain(domain_name)
#                     this_point_domain.set_parent(this_class_domain)
#                     keypoint_domain_info[task_uid][category_id] = this_point_domain
#                     for point_ind, point_name in enumerate(points_names, start=1):
#                         this_point_label = Label(point_name)
#                         this_point_label.add_supercategory(this_label)
#                         this_point_domain.add_label(this_point_label, ori_id=point_ind)
#                     this_point_domain.set_attributes("Skeleton", skeleton)  # TODO: 还没实现attributes的format
#         return parent_class_domain, (label_domain_info, keypoint_domain_info), raw_task_info, None
#
#     def parse_ann_info(self):
#         samples = self._annotation_info["samples"]
#         sample_struct = Struct("KeyPointSample")  # 样本 struct
#         object_struct = Struct("KeyPointLocalObject")  # 目标struct
#         media_field = Field("media", field_type="media")  # 图像 field
#         sample_struct.add_field(media_field)  # 添加图像field
#         sample_container = DataSample(sample_struct, None)  # 暂时不添加 class domain
#         domain_info = {}  # true_task_uid: domain
#         key_info = {}
#         field_args = {}  # true_task_uid: arg
#
#         for sample in tqdm(samples, desc="parsing samples ...."):
#             sample_item = {}  # 存储当前样本信息
#             media_info = sample["media"]
#             img_path = media_info.pop("path")
#             sample_item["media"] = img_path  # 添加图像样本信息
#             for k, v in media_info.items():  # 添加图像相关的attributes
#                 this_field = Field(k, field_value=v, is_attr=True)
#                 sample_struct.add_field(this_field)
#                 sample_item[k] = v
#
#             if "ground_truth" in sample:
#                 gt_info = sample["ground_truth"]
#             else:
#                 gt_info = []
#                 # sample_struct.set_optional("annotations")
#             annotations = []  # 用来装当前sample的所有的object
#             gt_info_dic = {}  # ann_id: {gt}
#             for gt in gt_info:
#                 # 获取ann_id
#                 task_type, task_name, ann_source = gt.pop("type"), gt.pop("name"), gt.pop("source")
#                 if task_type not in (self.INSTANCE_SEG_ANN_TYPE, self.DETECTION_ANN_TYPE, self.KEYPOINT2D_ANN_TYPE):
#                     continue
#
#                 ann_id = gt.pop("ann_id")
#                 ann_id = gt.pop("ref_ann_id", ann_id)
#                 gt_info_dic.setdefault(ann_id, {})
#                 gt_item = gt_info_dic[ann_id]
#                 task_uid = f"{task_type}${task_name}${ann_source}"
#
#                 # 写attributes
#                 attributes = gt.pop("attributes", {})
#                 for attr_k, attr_v in attributes.items():
#                     attr_k = Util.clean(attr_k)
#                     attr_field = Field(attr_k, field_value=attr_v, is_attr=True)
#                     object_struct.add_field(attr_field, optional=True)
#                     gt_item[attr_k] = attr_v
#
#                 if task_type == self.KEYPOINT2D_ANN_TYPE:
#                     if task_uid not in domain_info:
#                         category_id = gt.pop("category_id")
#                         domain_info.setdefault(task_uid, dict)
#                         domain_info[task_uid][category_id] = self._class_domain[1][task_uid][category_id]
#
#                     if len(field_args) == 0:
#                         arg = 'cdom'
#                         field_args[task_uid] = arg
#                     elif task_uid in field_args:
#                         arg = field_args[task_uid]
#                     else:
#                         arg = f"cdom{len(field_args)}"
#                         field_args[task_uid] = arg
#
#                     keypoint_field = Field("keypoints", field_type="keypoint", param=f"${arg}")
#                     gt_item["keypoints"] = gt.pop("points")
#                     object_struct.add_field(keypoint_field)
#
#                 elif task_type == self.DETECTION_ANN_TYPE:
#                     if 'categories' in gt and len(gt['categories']) > 0:
#                         label_field = Field("category", field_type="category", param=)
#
#                 domain_info[true_uid] = class_domain
#                 if len(key_info) == 0:
#                     map_field_name = "map_path"
#                     key_info[true_uid] = map_field_name
#                 elif true_uid in key_info:
#                     map_field_name = key_info[true_uid]
#                 else:
#                     map_field_name = f"map_path_{len(key_info)}"
#                     key_info[true_uid] = map_field_name
#                 if len(field_args) == 0:
#                     arg = "cdom"
#                     field_args[true_uid] = arg
#                 elif true_uid in field_args:
#                     arg = field_args[true_uid]
#                 else:
#                     arg = f"cdom{len(field_args)}"
#                     field_args[true_uid] = arg
#                 seg_map_field = Field(map_field_name, field_type="map_path", param=f"${arg}")
#                 sample_struct.add_field(seg_map_field)
#                 gt_item[map_field_name] = gt.pop('map_path')
#
#                 attributes = gt.pop("attributes", {})
#                 for attr_k, attr_v in attributes.items():
#                     attr_k = Util.clean(attr_k)
#                     attr_field = Field(attr_k, field_value=attr_v, is_attr=True)
#                     sample_struct.add_field(attr_field, optional=True)
#                     gt_item[attr_k] = attr_v
#                 sample_item.update(gt_item)
#
#             sample_container.add_item(sample_item, not self.separate_flag)
#         uids = list(key_info.keys())
#         field_args = [field_args[_] for _ in uids]
#         domains = [domain_info[_] for _ in uids]
#         sample_struct.set_arg(field_args)
#         sample_container.set_domain(domains)
#         return (sample_struct,), domains, sample_container
