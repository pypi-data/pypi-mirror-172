# encoding: utf-8
"""
@project: djangoModel->role_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色服务
@created_time: 2022/9/2 15:37
"""
from django.core.paginator import Paginator
from django.db.models import F

from ..models import Role, UserToRole
from ..utils.model_handle import format_params_handle


# 用户组 树状数据返回
class RoleTreeService(object):
    @staticmethod
    def get_tree(data_list, parent_group):
        tree = []
        for item in data_list:
            if str(item['parent_role_id']) == str(parent_group):
                item['name'] = item['role_name']
                item['children'] = RoleTreeService.get_tree(data_list, item['id'])
                tree.append(item)
        return tree

    @staticmethod
    def get_trees(data_list, parent_group):
        # 适配模式进行 搜索
        tree = []
        if parent_group != 0:  # 不从根节点搜索，自定义搜索
            base_node = Role.objects.filter(id=parent_group).to_json()  # 如果是搜索，则获取该节点角色信息
            for item in data_list:
                if str(item['parent_role_id']) == str(parent_group):
                    item['name'] = item['role_name']
                    item['children'] = RoleTreeService.get_tree(data_list, item['id'])
                    tree.append(item)
            base_node[0]['children'] = tree
            return base_node[0]
        else:  # 进行根节点搜索
            for item in data_list:
                if not str(item['parent_role_id']) == str(parent_group):
                    continue
                child = RoleTreeService.get_tree(data_list, item['id'])
                item['name'] = item['role_name']
                item['children'] = child
                tree.append(item)
        return tree

    @staticmethod
    def role_tree(role_id=0):
        data_list = list(Role.objects.all().values())
        group_tree = RoleTreeService.get_trees(data_list, role_id)
        return group_tree, None


class RoleService:
    @staticmethod
    def get_role_list(params, need_pagination=True):
        # 不分页查询
        if not need_pagination:
            params = format_params_handle(
                param_dict=params,
                filter_filed_list=["id", "id_list", "permission_id", "user_group_id", "user_group_id_list"],
                alias_dict={"id_list": "id__in", "user_group_id_list": "user_group_id__in"}
            )
            # print("params:", params)
            query_set = Role.objects.filter(**params)
            if not query_set:
                return [], None
            user_list = list(query_set.values())
            for i in user_list:
                id(i)
                i["is_role"] = True
                i["name"] = i["role_name"]
            return user_list, None
        # 分页查询
        page = params.pop("page", 1)
        size = params.pop("size", 20)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "permission_id", "role", "user_group_id", "page", "size"]
        )
        query_set = Role.objects.filter(**params).values()
        count = query_set.count()
        finish_set = list(Paginator(query_set, size).page(page).object_list)
        return {'size': int(size), 'page': int(page), 'count': count, 'list': finish_set}, None
        # return finish_set, None

    @staticmethod
    def user_role_list(user_id):
        return list(UserToRole.objects.filter(user_id=user_id).annotate(
            role_value=F('role_id__role'),
            role_name=F('role_id__role_name'),
            permission_id=F('role_id__permission'),
            permission_name=F('role_id__permission__permission_name'),
            user_group_value=F('role_id__user_group__group'),
            user_group_name=F('role_id__user_group__group_name'),
        ).values('id', 'role_id', 'user_id', 'role_value', 'role_name', 'permission_id', 'permission_name',
                 'user_group_value', 'user_group_name'))

    @staticmethod
    def user_list_by_roles(role_list):
        """按角色ID获取相关用户列表"""
        return list(UserToRole.objects.filter(role_id__in=role_list).values() or [])

    @staticmethod
    def user_bind_role(user_id, role_id):
        # 用户绑定角色
        if not user_id or not role_id:
            return None, "参数错误，user_id, role_id 必传"
        try:
            UserToRole.objects.get_or_create(
                {"user_id": user_id, "role_id": role_id},
                user_id=user_id,
                role_id=role_id,
            )
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def bind_user_role(user_id, role_list):
        if not role_list:
            UserToRole.objects.filter(user_id=user_id).delete()
            return None, None
        list = role_list.split(',')
        UserToRole.objects.filter(user_id=user_id).delete()
        try:
            for i in list:
                data = {
                    "user_id": user_id,
                    "role_id": i
                }
                UserToRole.objects.create(**data)
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def add_role(params):
        params = format_params_handle(param_dict=params,
                                      filter_filed_list=["role", "role_name", "parent_role_id", "permission_id",
                                                         "user_group_id", "description"])
        if not params:
            return None, "参数不能为空"
        instance = Role.objects.create(**params)
        return {"id": instance.id}, None

    @staticmethod
    def edit_role(params):
        params = format_params_handle(param_dict=params,
                                      filter_filed_list=["role_id", "role", "role_name", "parent_role_id",
                                                         "permission_id",
                                                         "user_group_id", "description"])
        id = params.pop("role_id", None)
        if not id:
            return None, "ID 不可以为空"
        if not params:
            return None, "没有可以修改的字段"
        instance = Role.objects.filter(id=id)
        if params:
            instance.update(**params)
        return None, None

    @staticmethod
    def del_role(id):
        if not id:
            return None, "ID 不可以为空"

        user_role_set = UserToRole.objects.filter(role_id=id).exists()
        if user_role_set:
            return None, "该角色有绑定关系,无法删除"
        instance = Role.objects.filter(id=id)
        if instance:
            instance.delete()
        return None, None
