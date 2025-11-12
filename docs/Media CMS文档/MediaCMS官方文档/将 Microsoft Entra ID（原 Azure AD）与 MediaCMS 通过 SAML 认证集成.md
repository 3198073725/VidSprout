# 将 Microsoft Entra ID（原 Azure AD）与 MediaCMS 通过 SAML 认证集成

本指南提供了分步说明，指导如何将 Microsoft Entra ID 配置为 MediaCMS（一个开源内容管理系统）的 SAML 身份提供商（IdP）。目标是实现安全、可扩展的用户单点登录（SSO）认证。

## 目录

1. [概述](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#概述)
2. [前置条件](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#前置条件)
3. [步骤 1：为 MediaCMS 配置 SAML](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#步骤-1为-mediacms-配置-saml)
4. [步骤 2：在 Entra ID 中将 MediaCMS 注册为企业应用](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#步骤-2在-entra-id-中将-mediacms-注册为企业应用)
5. [步骤 3：在 Entra ID 中配置 SAML 设置](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#步骤-3在-entra-id-中配置-saml-设置)
6. [步骤 4：在 MediaCMS 中配置 SAML 设置](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#步骤-4在-mediacms-中配置-saml-设置)
7. [步骤 5：允许用户或组登录应用程序](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#步骤-5允许用户或组登录应用程序)
8. [步骤 6：测试和验证登录流程](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#步骤-6测试和验证登录流程)
9. [故障排除](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#故障排除)
10. [资源](https://tencent.yuanbao/chat?from=launch&conversation=ed4a9539-66dd-429d-ad1f-fd1702c73239&project_id=&project_name=&HY82=2&HY56=SlidePage#资源)

------

## 概述

MediaCMS 通过充当服务提供商（SP）来支持 SAML 2.0 认证。通过与 Microsoft Entra ID 集成，组织可以允许用户使用其现有的企业凭据进行认证。

在我们特定的 MediaCMS 部署中，应用程序托管在内部，无法从公共互联网直接入站访问。作为一个内部公司应用程序，将其与现有的认证系统集成并提供无缝的单点登录体验至关重要。这正是 SAML 协议的用武之地。

SAML 认证的一个主要优势是，身份提供商（IdP）——本例中为 Microsoft Entra ID——和服务提供商（SP）——MediaCMS——之间的所有通信完全由最终用户的浏览器代理。浏览器启动认证流程，与 Microsoft 的登录门户安全通信，接收身份断言，然后将其传递回内部的 MediaCMS 服务器。

这种架构使得 MediaCMS 服务器能够保持与互联网隔离，同时仍然参与现代且无缝的联合登录体验。

尽管本教程中概述的部署方法是针对隔离的 MediaCMS 服务器上的 Entra ID，但相同的步骤和一般信息也可以应用于非隔离系统上的其他 SAML 提供商/身份提供商。

> **注意**：本指南假设您正在运行带有 Django 后端的 MediaCMS，并且已启用并配置了 `django-allauth`库。

------

## 前置条件

开始之前，请确保满足以下条件：

- 您拥有 MediaCMS 和 Microsoft Entra ID（Azure 门户）的管理员访问权限。
- MediaCMS 已安装并通过 HTTPS 访问，且拥有有效的 SSL 证书。
- 您的 MediaCMS 安装已启用 SAML 支持（通过 `django-allauth`）。
- 您拥有 MediaCMS 的专用域或子域（例如，`https://<MyMediaCMS.MyDomain.com>`）。

------

## 步骤 1：为 MediaCMS 配置 SAML

启用 SAML 认证的第一步是修改您的 MediaCMS 部署的 `local_settings.py`文件（对于 Docker：`./deploy/docker/local_settings.py`）。添加以下配置块以启用 SAML 支持、基于角色的访问控制（RBAC）并强制执行安全通信设置：

```
USE_RBAC = True
USE_SAML = True
USE_IDENTITY_PROVIDERS = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

SOCIALACCOUNT_ADAPTER = 'saml_auth.adapter.SAMLAccountAdapter'
SOCIALACCOUNT_PROVIDERS = {
    "saml": {
        "provider_class": "saml_auth.custom.provider.CustomSAMLProvider",
    }
}
```

这些设置启用了 SAML 认证，配置 MediaCMS 以遵循基于角色的访问控制，并应用了重要的头部和 Cookie 策略以确保安全的浏览器处理——所有这些对于 SAML 流程的正常运行都是必需的。

> ⚠⚠⚠️ **重要提示**：更新 `local_settings.py`文件后，您必须重新启动 MediaCMS 服务（例如，通过重启 Docker 容器）才能使更改生效。此步骤必须在继续下一个配置阶段之前完成。

------

## 步骤 2：在 Entra ID 中将 MediaCMS 注册为企业应用

要在 Microsoft Entra ID（原 Azure AD）端开始集成过程，请按照以下步骤将 MediaCMS 注册为新的企业应用程序。

### 1. 导航到企业应用程序

- 登录您的 [Azure 门户](https://portal.azure.com/)。
- 导航到 **企业应用程序**。

> *注意：本指南假设您已有一个现有的 Azure 租户，并且 Entra ID 已配置了用户和组。*

### 2. 创建新应用程序

- 点击 **+ 新建应用程序** 按钮。
- 在下一个屏幕上，选择 **创建您自己的应用程序**。
- 输入应用程序的名称（例如，`MediaCMS`）。
- 在"您希望用您的应用程序做什么？"下，选择 **集成您在图库中找不到的任何其他应用程序（非图库）**。
- 点击 **创建**。

片刻之后，Azure 将创建新应用程序并将您重定向到其配置页面。

------

## 步骤 3：在 Entra ID 中配置 SAML 设置

### 1. 配置基于 SAML 的单点登录

- 从应用程序概览页面，在左侧菜单的 **管理** 下，点击 **单点登录**。
- 系统将提示您选择登录方法。选择 **SAML**。

### 2. 选择客户端 ID 名称

在填写 SAML 配置之前，您必须决定一个客户端 ID 名称。此名称将唯一标识您的 SAML 集成，并出现在您的登录 URL 中。

- 选择一个描述性强且易于记忆的名称（例如，`mediacms_entraid`）。
- 您将在 MediaCMS 和 Entra ID 配置设置中使用此名称。

### 3. 填写基本 SAML 配置

现在在 **基本 SAML 配置** 部分输入以下值：

| 字段                   | 值                                                           |
| ---------------------- | ------------------------------------------------------------ |
| **标识符(实体 ID)**    | `https://<MyMediaCMS.MyDomain.com>/saml/metadata/`           |
| **回复 URL (ACS URL)** | `https://<MyMediaCMS.MyDomain.com>/accounts/saml/<MyClientID>/acs/` |
| **登录 URL**           | `https://<MyMediaCMS.MyDomain.com>/accounts/saml/<MyClientID>/login/` |
| **中继状态 (可选)**    | `https://<MyMediaCMS.MyDomain.com>/`                         |
| **注销 URL (可选)**    | `https://<MyMediaCMS.MyDomain.com>/accounts/saml/<MyClientID>/sls/` |

> 🔐🔐 如果不同，请将 `<MyClientID>`替换为您自己选择的客户端 ID。

填写完这些字段后，保存您的配置。

保持 Azure 企业应用程序单点登录配置窗口打开，因为我们现在要将此 Azure 页面中的一些详细信息配置到我们的 MediaCMS 系统中。

------

## 步骤 4：在 MediaCMS 中配置 SAML 设置

在 MediaCMS 中，首先登录后端管理网页。您将在左侧菜单栏下看到新的选项。

### 1. 添加登录选项

- 导航到 **身份提供商 → 登录选项**。

- 点击 **添加登录选项**。

- 为登录选项指定一个标题。此标题可以是任何您喜欢的名称，但它会在最终用户选择登录方法时显示给他们，因此请确保名称清晰（例如，`EntraID-SSO`）。

- 将 **登录 URL** 设置为与之前相同的登录 URL：

  ```
  https://<MyMediaCMS.MyDomain.com>/accounts/saml/<MyClientID>/login/
  ```

- 如果您没有其他认证方法，请将排序保留为 `0`。

- 确保勾选 **活跃** 框，使此登录方法处于活动状态。

- 点击 **保存** 继续。

### 2. 添加 ID 提供商

- 导航到 **身份提供商 → ID 提供商**。
- 点击 **添加 ID 提供商**。

回到您的 Azure 企业应用程序配置窗口（在单点登录配置菜单的底部），找到您的应用程序特定详细信息。它们看起来像下面的示例：

```
示例唯一 AppID: 123456ab-1234-12ab-ab12-abc123abc123
唯一 AppID 在您创建应用程序时自动生成。

-- 示例 URL --
登录 URL: https://login.microsoftonline.com/123456ab-1234-12ab-ab12-abc123abc123/saml2
Microsoft Entra 标识符: https://sts.windows.net/123456ab-1234-12ab-ab12-abc123abc123/
注销 URL: https://login.microsoftonline.com/123456ab-1234-12ab-ab12-abc123abc123/saml2
```

回到 MediaCMS 的新建 ID 提供商窗口，在 **常规** 选项卡下：

- **协议**：`saml`（全部小写）
- **提供商 ID**：Microsoft Entra 标识符（如上所示），整个 URL。
- **IDP 配置名称**：任何唯一名称（例如，`EntraID`）
- **客户端 ID**：与您之前在配置 Entra ID 时使用的客户端 ID 完全相同（例如，`mediacms_entraid`）。
- **站点**：添加您希望此登录选项出现的所有站点（例如，所有站点）

点击 **保存并继续**，然后转到 **SAML 配置** 选项卡。

在 **SAML 配置** 选项卡上：

- **SSO URL**：使用上面列出的 Entra ID 示例中的相同登录 URL。

- **SLO URL**：使用上面列出的 Entra ID 示例中的注销 URL。

- **SP 元数据 URL**：

  ```
  https://<MyMediaCMS.MyDomain.com>/saml/metadata/
  ```

- **IdP ID**：使用上面列出的相同的 Microsoft Entra 标识符 URL。

#### LDP 证书

回到 Azure 企业应用程序页面（SAML 证书部分），下载 **Base64 证书**，在文本编辑器中打开它，并将其内容复制到 MediaCMS 中的 **LDP 证书** 设置里。

### 3. 配置身份映射

映射 Entra ID 将提供给 MediaCMS 的身份属性。尽管只有 UID 被指定为必填项，但除非所有详细信息都已填写，否则 Entra ID 将无法工作（是的，您必须在字段中键入 NA；不能留空。如果不这样做，您将收到 500 错误）。您可以使用下面的确切设置：

| 字段           | 值                                                           |
| -------------- | ------------------------------------------------------------ |
| **Uid**        | `http://schemas.microsoft.com/identity/claims/objectidentifier` |
| **Name**       | `http://schemas.microsoft.com/identity/claims/displayname`   |
| **Email**      | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress` |
| **Groups**     | `NA`                                                         |
| **First name** | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname` |
| **Last name**  | `http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname` |
| **User logo**  | `NA`                                                         |
| **Role**       | `NA`                                                         |

> ℹℹ️ 组和角色可以在 Azure 企业应用程序中的 **属性和声明** 下更改或重新映射。

勾选 **已验证电子邮件** 框（因为 Entra ID 将为您验证用户）。在设置过程中，您可以启用 **保存 SAML 响应日志** 以用于故障排除。

最后，点击 **保存** 完成新 ID 提供商的添加。

------

## 步骤 5：允许用户或组登录应用程序

回到 Azure AD 内部，在您的 MediaCMS 企业应用程序中，您必须分配允许使用 MediaCMS 认证登录的用户或组。

### 1. 导航到用户和组

- 打开 Azure 门户并转到您的 **MediaCMS 企业应用程序**。
- 在左侧的 **管理** 菜单中，点击 **用户和组**。

### 2. 分配用户或组

- 添加允许使用 Entra ID 认证方法登录 MediaCMS 的单个用户或用户组。
- 在本示例中，通过使用特殊组 **所有用户**，该应用程序被提供给 Entra ID 中的所有注册用户，这授予租户中的任何注册用户访问 MediaCMS 的权限。

> ⚠⚠⚠️ **重要提示**：嵌套组将不起作用。所有用户必须直接分配到您授予权限的组。如果一个组包含另一个组，则嵌套组的用户不会从父组继承使用此应用程序的权限。

------

## 步骤 6：测试和验证登录流程

此时，您应该访问您的 MediaCMS 网页，尝试使用刚刚设置的认证方法登录。

------

## 故障排除

如果您遇到登录问题，首先直接查看 SAML 认证数据会很有帮助。

1. 转到 MediaCMS 的登录页面。它应该将您重定向到 Microsoft 的登录页面。
2. 在完成 Microsoft 认证之前，打开 Firefox 或 Chrome 开发者工具（按 **F12**）并导航到 **网络** 选项卡。
3. 启用 **持续记录**。
4. 在您的页面上完成 Microsoft 认证步骤（包括如果启用了双因素认证）。

在认证的最后一步（通常在输入代码并确认"保持登录状态？"之后），您将看到几个 POST 请求返回到您的 MediaCMS 服务器 URL。找到发送到您的 MediaCMS 服务器的断言消费者服务（ACS）URL 的 POST 请求，该 URL 如下所示：

```
https://<MyMediaCMS.MyDomain.com>/accounts/saml/<MyClientID>/acs/
```

在网络选项卡的请求部分，您将看到一个标记为 **SAMLResponse** 的 **表单数据** 字段，其中包含来自 Entra ID 的经过 Base64 编码的 XML 格式的认证断言。

- 点击 SAML 响应的数据字段，以便您可以突出显示并复制所有 Base64 编码的文本。
- 然后，您可以将此 Base64 编码的文本带到像 [CyberChef](https://gchq.github.io/CyberChef/)这样的工具中，使用 **From Base64** 解码器和 **XML Beautify** 来显示 XML 格式的 SAML 响应。

此解码后的 XML 包含传递回 MediaCMS 的所有断言和令牌详细信息。您可以使用此信息来排除出现的任何问题或配置错误。

您还可以通过打开一个私人浏览窗口并导航到以下 URL 来确认您的 MediaCMS 服务器具有正确的 SAML 认证设置，该 URL 将输出您的 MediaCMS 服务器当前配置的 XML 数据：

```
https://<MyMediaCMS.MyDomain.com>/saml/metadata/
```

您可以使用从此 URL 返回的 XML 数据来确认 MediaCMS 是否按预期进行了适当配置，并向身份提供商提供了正确的信息。

### 无限重定向循环

您可能遇到的另一个问题是 **无限重定向循环**。当强制全局登录且本地用户登录被禁用时，可能会发生这种情况。

**症状：** 系统在主页和登录 URL 之间持续重定向。

**根本原因：** 由于需要全局登录且本地登录被禁用，Django 尝试将用户重定向到默认的本地登录页面。由于该登录方法不可用，用户被弹回主页，再次触发相同的重定向逻辑——导致循环。

**解决方案：** 在您的本地设置中指定正确的 SAML 认证 URL。例如：

- 在 MediaCMS 中为 Entra ID 配置的"登录选项" URL：

  ```
  https://<MyDomainName>/accounts/saml/mediacms_entraid/login/
  ```

- 将以下行添加到 `./deploy/docker/local_settings.py`：

  ```
  LOGIN_URL = "/accounts/saml/mediacms_entraid/login/"
  ```

此更改确保 Django 使用正确的 SAML 登录路由，打破重定向循环，并允许按预期通过 Entra ID 进行认证。

> **注意：** `LOGIN_URL`设置有效是因为我们使用 Django AllAuth 模块来执行 SAML 认证。如果您查看 AllAuth Django 配置设置，您会发现这是一个可以通过本地设置文件设置的选项，Django 在使用 AllAuth 模块时会读取该文件。您可以通过以下 URL 查看模块文档以获取更多详细信息和可以通过 `local_settings.py`通过 AllAuth 设置的其他设置：https://django-allauth.readthedocs.io/en/latest/account/configuration.html

------

## 资源

- [MediaCMS SAML 文档](https://github.com/mediacms-io/mediacms/blob/main/docs/admins_docs.md#24-identity-providers-setup)
- [为企业应用程序启用 SAML 单点登录](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/add-application-portal-setup-sso)
- [Django AllAuth](https://django-allauth.readthedocs.io/en/latest/index.html)

------

*本文档是一个进行中的工作，将根据进一步的步骤说明或完成情况进行更新。*