# Bruker NIR Spectrum Converter

简体中文 | [English](README_EN.md)

将布鲁克(Bruker) OPUS光谱仪的 `.0` 格式近红外光谱文件转换为通用TXT格式的工具。

## 功能特点

- ✅ 支持布鲁克OPUS `.0` 格式光谱文件解析
- ✅ 自动提取波长/波数和吸光度数据
- ✅ 支持批量转换目录下所有文件
- ✅ 输出包含波数(cm⁻¹)、波长(nm)和吸光度
- ✅ 纯Python实现，无外部依赖（仅需NumPy）

## 支持的光谱范围

| 参数 | 值 |
|------|-----|
| 波长点数 | 1899 |
| 波数范围 | 3948 - 11540 cm⁻¹ |
| 波长范围 | 866.6 - 2532.9 nm |

## 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/bruker-nir-converter.git
cd bruker-nir-converter

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 命令行转换

```bash
# 转换单个文件
python bruker_converter.py path/to/spectrum.0

# 转换整个目录
python bruker_converter.py path/to/spectra_folder

# 指定输出目录
python bruker_converter.py path/to/spectra_folder output_folder
```

### Python代码中使用

```python
from bruker_converter import parse_bruker_spectrum, save_to_txt

# 解析光谱文件
wavenumbers, wavelengths, absorbance_data, npt = parse_bruker_spectrum('spectrum.0')

# 保存为TXT
save_to_txt('output.txt', wavenumbers, wavelengths, absorbance_data, npt)
```

## 输出格式

转换后的TXT文件格式如下：

```txt
# ========================================
# Bruker NIR Spectrum Data Converter
# ========================================
#
# Data points: 1899
# Wavenumber range: 3948.0 - 11540.0 cm-1
# Wavelength range: 2532.9 - 866.6 nm
#
# Format: Wavenumber(cm-1) | Wavelength(nm) | Absorbance
# ========================================
11540.0000	866.5511	0.000000
11536.0000	866.8516	0.000000
...
```

## 文件格式解析

本工具解析布鲁克OPUS `.0` 格式文件的以下参数：

| 参数 | 文件偏移 | 数据类型 |
|------|----------|----------|
| 波长点数 (NPT) | 0x46c | int16 |
| 开始波数 (FXV) | 0x478 | float64 |
| 结束波数 (LXV) | 0x488 | float64 |
| 吸光度数据 | 0x24c00 | float32[] |

## 测试

项目包含测试文件 `test/test.0`，可用于验证转换功能：

```bash
python bruker_converter.py test/
```

## 依赖

- Python 3.7+
- NumPy

## 许可证

MIT License - 请自由使用和修改

## 作者

Matrix Agent

## 参考

- [Matlab解析布鲁克.o格式光谱文件](https://blog.csdn.net/NIR_cloud/article/details/128788340)
