# 积木产品图自动生成项目

这个项目可以读取 `products.csv` 和 `input_images` 文件夹里的产品参考图，然后每个 SKU 自动生成 6 张产品图，保存到 `output/SKU/`。

生成文件名固定为：

1. `01_Hero.png`
2. `02_ProductSize.png`
3. `03_DetailDisplay.png`
4. `04_BuildExperience.png`
5. `05_MoodShot.png`
6. `06_DisplayLife.png`

## 1. 准备 Python

建议使用 Python 3.10 或更高版本。

查看版本：

```bash
python --version
```

## 2. 安装依赖

在项目目录运行：

```bash
pip install -r requirements.txt
```

## 3. 配置 OpenAI API Key

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

打开 `.env`，把下面这一行改成你自己的 Key：

```env
OPENAI_API_KEY=sk-your-api-key-here
```

默认模型已经设置为：

```env
OPENAI_IMAGE_MODEL=gpt-image-1
```

## 4. 放入产品参考图

把产品参考图放到 `input_images/` 文件夹。

支持格式：

- `.png`
- `.jpg`
- `.jpeg`
- `.webp`

## 5. 填写 products.csv

`products.csv` 字段固定，不能改字段名和顺序：

```csv
sku,product_name,pcs,length,width,height,image_path
DEMO001,示例积木产品,500,20,15,12,demo.jpg
```

字段说明：

| 字段 | 说明 |
| --- | --- |
| `sku` | 产品 SKU，会用于创建输出文件夹 |
| `product_name` | 产品名称 |
| `pcs` | 颗粒数 |
| `length` | 长度，建议填厘米 |
| `width` | 宽度，建议填厘米 |
| `height` | 高度，建议填厘米 |
| `image_path` | 参考图文件名，例如 `demo.jpg` |

如果 `image_path` 为空，程序会尝试在 `input_images/` 中按 SKU 找图，例如：

- `DEMO001.png`
- `DEMO001.jpg`
- `DEMO001.jpeg`
- `DEMO001.webp`

## 6. 运行生成

```bash
python main.py
```

生成完成后，查看：

```text
output/你的SKU/
```

例如：

```text
output/DEMO001/01_Hero.png
output/DEMO001/02_ProductSize.png
output/DEMO001/03_DetailDisplay.png
output/DEMO001/04_BuildExperience.png
output/DEMO001/05_MoodShot.png
output/DEMO001/06_DisplayLife.png
```

## 7. 后续填写正式提示词

现在 `prompt_templates.py` 里已经准备好 6 个空模板函数：

- `hero_prompt()`
- `size_prompt()`
- `detail_prompt()`
- `build_prompt()`
- `mood_prompt()`
- `display_prompt()`

你后面把最终提示词发来后，可以直接填到这 6 个函数里。

在模板函数还是空字符串时，程序会自动使用 `image_generator.py` 里的基础兜底提示词，所以项目现在也可以运行。

## 常见问题

### 运行时报错：没有找到 OPENAI_API_KEY

请确认你已经复制 `.env.example` 为 `.env`，并且 `.env` 里填了真实 API Key。

### 参考图不存在怎么办

程序会提示警告，并且不带参考图生成图片。建议检查：

- 图片是否已经放到 `input_images/`
- `products.csv` 里的 `image_path` 是否写对
- 文件后缀是否正确

### 生成图片要花钱吗

会。调用 OpenAI 图片生成 API 会按 OpenAI 账号计费，请先确认你的账号额度和计费设置。
