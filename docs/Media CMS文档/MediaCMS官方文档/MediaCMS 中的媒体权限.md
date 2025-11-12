# MediaCMS 中的媒体权限

本文档解释了 MediaCMS 中的权限系统，该系统控制谁可以查看、编辑和管理媒体文件。

## 概述

MediaCMS 提供了一个灵活的权限系统，允许对媒体访问进行细粒度控制。该系统支持：

1. **基本权限** - 公开、私有和未列出的媒体
2. **用户特定权限** - 授予特定用户的直接权限
3. **基于角色的访问控制（RBAC）** - 通过组成员身份实现的基于类别的权限

## 媒体状态

每个媒体文件都有一个决定其基本可见性的状态：

- **公开** - 对所有人可见
- **私有** - 仅对所有者以及拥有明确权限的用户可见
- **未列出** - 不会在公开列表中显示，但可以通过直接链接访问

## 用户角色

MediaCMS 有多个影响权限的用户角色：

- **普通用户** - 可以上传和管理自己的媒体
- **高级用户** - 具有额外能力（可配置）
- **MediaCMS 编辑者** - 可以跨平台编辑和审查内容
- **MediaCMS 管理者** - 拥有完整的管理能力
- **管理员** - 拥有完整的系统访问权限

## 直接媒体权限

`MediaPermission`模型允许向单个用户授予特定权限：

### 权限级别

- **查看者** - 可以查看媒体，即使其为私有状态
- **编辑者** - 可以查看和编辑媒体的元数据
- **所有者** - 完全控制，包括删除

## 基于角色的访问控制（RBAC）

当启用 RBAC（通过 `USE_RBAC`设置）时，可以通过类别和组来管理权限：

1. 类别可以标记为 RBAC 控制
2. 用户被分配到具有特定角色的 RBAC 组中
3. RBAC 组与类别相关联
4. 用户根据其角色继承对这些类别中媒体的权限

### RBAC 角色

- **成员** - 可以查看类别中的媒体
- **贡献者** - 可以查看和编辑类别中的媒体
- **管理者** - 对类别中的媒体拥有完全控制权

## 权限检查方法

用户模型提供了几种检查权限的方法：

```
# 来自 users/models.py
def has_member_access_to_media(self, media):
    # 检查用户是否可以查看该媒体
    # ...

def has_contributor_access_to_media(self, media):
    # 检查用户是否可以编辑该媒体
    # ...

def has_owner_access_to_media(self, media):
    # 检查用户是否对该媒体拥有完全控制权
    # ...
```

## 权限应用方式

当用户尝试访问媒体时，系统按以下顺序检查权限：

1. 媒体是公开的吗？如果是，允许访问。
2. 用户是该媒体的所有者吗？如果是，允许完全访问。
3. 用户是否通过 MediaPermission 拥有直接权限？如果是，授予相应的访问级别。
4. 如果启用了 RBAC，用户是否通过类别成员身份拥有访问权限？如果是，授予相应的访问级别。
5. 如果以上都不是，则拒绝访问。

## 媒体共享

用户可以通过以下方式与他人共享媒体：

1. 将其设置为公开或未列出
2. 向特定用户授予直接权限
3. 将其添加到 RBAC 组可访问的类别中

## 实现细节

### 媒体列表

在列出媒体时，系统会基于权限进行过滤：

```
# 简化示例，来自 files/views/media.py
def _get_media_queryset(self, request, user=None):
    # 1. 公开媒体
    listable_media = Media.objects.filter(listable=True)

    if not request.user.is_authenticated:
        return listable_media

    # 2. 已认证用户的用户权限
    user_media = Media.objects.filter(permissions__user=request.user)

    # 3. 已认证用户的 RBAC 权限
    if getattr(settings, 'USE_RBAC', False):
        rbac_categories = request.user.get_rbac_categories_as_member()
        rbac_media = Media.objects.filter(category__in=rbac_categories)

    # 合并所有可访问的媒体
    return listable_media.union(user_media, rbac_media)
```

### 权限检查

系统使用辅助方法来检查权限：

```
# 来自 users/models.py
def has_member_access_to_media(self, media):
    # 首先检查用户是否是所有者
    if media.user == self:
        return True

    # 然后检查 RBAC 权限
    if getattr(settings, 'USE_RBAC', False):
        rbac_groups = RBACGroup.objects.filter(
            memberships__user=self,
            memberships__role__in=["member", "contributor", "manager"],
            categories__in=media.category.all()
        ).distinct()
        if rbac_groups.exists():
            return True

    # 然后检查 MediaShare 权限（任何访问级别）
    media_permission_exists = MediaPermission.objects.filter(
        user=self,
        media=media,
    ).exists()

    return media_permission_exists
```

## 最佳实践

1. **默认为私有** - 考虑将新上传的媒体默认设置为私有
2. **使用类别** - 将媒体组织到类别中，以便更轻松地管理权限
3. **团队协作使用 RBAC** - 在团队协作场景中使用 RBAC
4. **例外情况使用直接权限** - 对于一次性共享使用直接权限

## 配置

权限系统可以通过以下几个设置进行配置：

- `USE_RBAC`- 启用/禁用基于角色的访问控制

## 结论

MediaCMS 提供了一个灵活而强大的权限系统，可以适应各种用例，从简单的个人媒体库到具有细粒度访问控制的复杂团队协作场景。