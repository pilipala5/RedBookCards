#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ============================================
# build.py - 自动化打包脚本（修复版）
# ============================================

import os
import sys
import shutil
import subprocess
from pathlib import Path
import zipfile
from datetime import datetime
import importlib.util
import pkg_resources

class AppBuilder:
    """应用打包器"""
    
    def __init__(self):
        self.root_dir = Path.cwd()
        self.build_dir = self.root_dir / "build"
        self.dist_dir = self.root_dir / "dist"
        self.resources_dir = self.root_dir / "resources"
        self.icons_dir = self.resources_dir / "icons"
        
        # 应用信息
        self.app_name = "XiaohongshuEditor"
        self.app_version = "1.0.0"
        self.app_description = "小红书 Markdown 编辑器"
        
    def clean_build(self):
        """清理之前的构建文件"""
        print("🧹 清理旧的构建文件...")
        
        # 删除构建目录
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
            print(f"  ✓ 删除 {self.build_dir}")
            
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
            print(f"  ✓ 删除 {self.dist_dir}")
            
        # 删除 spec 文件
        spec_file = self.root_dir / f"{self.app_name}.spec"
        if spec_file.exists():
            spec_file.unlink()
            print(f"  ✓ 删除 {spec_file}")
            
        # 删除临时文件
        for pattern in ["*.pyc", "__pycache__", ".pytest_cache"]:
            for file in self.root_dir.rglob(pattern):
                if file.is_file():
                    file.unlink()
                elif file.is_dir():
                    shutil.rmtree(file)
                    
    def check_requirements(self):
        """检查依赖（改进版）"""
        print("\n📋 检查依赖...")
        
        # 依赖包映射（包名 -> 导入名）
        package_mapping = {
            "PySide6": "PySide6",
            "markdown": "markdown",
            "beautifulsoup4": "bs4",  # beautifulsoup4 实际导入名是 bs4
            "pyinstaller": "PyInstaller",  # 注意大小写
            "Pillow": "PIL"  # Pillow 实际导入名是 PIL
        }
        
        missing = []
        
        for package_name, import_name in package_mapping.items():
            try:
                # 方法1：尝试使用 pkg_resources 检查
                try:
                    pkg_resources.get_distribution(package_name)
                    found = True
                except pkg_resources.DistributionNotFound:
                    found = False
                
                # 方法2：如果方法1失败，尝试导入
                if not found:
                    spec = importlib.util.find_spec(import_name)
                    found = spec is not None
                
                # 方法3：对于特殊包的额外检查
                if not found and import_name == "PyInstaller":
                    # PyInstaller 可能作为命令行工具安装
                    result = subprocess.run(
                        [sys.executable, "-m", "PyInstaller", "--version"],
                        capture_output=True,
                        text=True
                    )
                    found = result.returncode == 0
                
                if found:
                    print(f"  ✓ {package_name}")
                else:
                    missing.append(package_name)
                    print(f"  ✗ {package_name} (缺失)")
                    
            except Exception as e:
                # 如果检查过程出错，尝试直接导入
                try:
                    __import__(import_name)
                    print(f"  ✓ {package_name}")
                except ImportError:
                    missing.append(package_name)
                    print(f"  ✗ {package_name} (缺失) - {e}")
                
        if missing:
            print(f"\n⚠️  缺少依赖包: {', '.join(missing)}")
            print("请运行以下命令安装:")
            print(f"  pip install {' '.join(missing)}")
            return False
            
        return True
        
    def verify_main_script(self):
        """验证主脚本是否存在"""
        print("\n📝 验证主脚本...")
        
        main_script = self.root_dir / "main.py"
        if not main_script.exists():
            print(f"  ✗ 找不到 main.py")
            print("  请确保 main.py 在项目根目录")
            return False
            
        print(f"  ✓ 找到 main.py")
        
        # 检查 src 目录结构
        src_dir = self.root_dir / "src"
        if not src_dir.exists():
            print(f"  ⚠️  找不到 src 目录，将创建基本结构")
            self.create_basic_structure()
            
        return True
        
    def create_basic_structure(self):
        """创建基本的项目结构"""
        print("\n🏗️  创建基本项目结构...")
        
        # 创建目录
        dirs = [
            "src/ui",
            "src/core",
            "src/utils",
            "resources/styles",
            "resources/templates",
            "resources/icons"
        ]
        
        for dir_path in dirs:
            path = self.root_dir / dir_path
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ 创建目录: {dir_path}")
            
        # 创建 __init__.py 文件
        for dir_path in ["src", "src/ui", "src/core", "src/utils"]:
            init_file = self.root_dir / dir_path / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# -*- coding: utf-8 -*-\n")
                print(f"  ✓ 创建文件: {dir_path}/__init__.py")
                
    def create_icon(self):
        """创建应用图标"""
        print("\n🎨 生成应用图标...")
        
        # 确保图标目录存在
        self.icons_dir.mkdir(parents=True, exist_ok=True)
        
        # 检查是否已有图标
        ico_file = self.icons_dir / "app.ico"
        if ico_file.exists():
            print(f"  ✓ 图标已存在: {ico_file}")
            return True
            
        # 运行图标生成脚本
        icon_script = self.root_dir / "create_icon.py"
        if icon_script.exists():
            try:
                subprocess.run([sys.executable, str(icon_script)], check=True)
                print("  ✓ 图标生成成功")
                return True
            except subprocess.CalledProcessError as e:
                print(f"  ⚠️  图标生成失败: {e}")
                print("  将继续打包（使用默认图标）")
                return False
        else:
            print("  ⚠️  找不到图标生成脚本")
            print("  将继续打包（使用默认图标）")
            return False
            
    def build_exe(self, mode="onefile"):
        """构建可执行文件
        
        Args:
            mode: "onefile" - 单文件模式, "onedir" - 文件夹模式
        """
        print(f"\n🔨 开始构建 ({mode} 模式)...")
        
        # 根据操作系统调整路径分隔符
        path_separator = ";" if sys.platform == "win32" else ":"
        
        # PyInstaller 命令
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",  # 清理临时文件
            "--noconfirm",  # 覆盖输出目录
        ]
        
        # 根据模式添加参数
        if mode == "onefile":
            cmd.append("--onefile")
        else:
            cmd.append("--onedir")
            
        # 添加其他参数
        cmd.extend([
            "--windowed",  # 窗口程序（无控制台）
            "--name", self.app_name,
        ])
        
        # 添加图标（如果存在）
        ico_file = self.icons_dir / "app.ico"
        if ico_file.exists():
            cmd.extend(["--icon", str(ico_file)])
        
        # 添加资源文件（如果存在）
        if self.resources_dir.exists():
            cmd.extend(["--add-data", f"{self.resources_dir}{path_separator}resources"])
        
        # 添加 src 目录（如果存在）
        src_dir = self.root_dir / "src"
        if src_dir.exists():
            cmd.extend(["--add-data", f"{src_dir}{path_separator}src"])
        
        # 添加隐藏导入
        hidden_imports = [
            "PySide6.QtCore",
            "PySide6.QtGui",
            "PySide6.QtWidgets",
            "PySide6.QtWebEngineCore",
            "PySide6.QtWebEngineWidgets",
            "markdown",
            "markdown.extensions",
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.nl2br",
            "markdown.extensions.attr_list",
            "markdown.extensions.def_list",
            "markdown.extensions.footnotes",
            "markdown.extensions.toc",
            "markdown.extensions.sane_lists",
            "markdown.extensions.smarty",
            "bs4",  # beautifulsoup4
        ]
        
        for imp in hidden_imports:
            cmd.extend(["--hidden-import", imp])
            
        # 排除不需要的模块
        excludes = ["tkinter", "matplotlib", "numpy", "pandas", "scipy", "test", "tests"]
        for exc in excludes:
            cmd.extend(["--exclude-module", exc])
            
        # 添加版本信息文件（如果存在）
        version_file = self.root_dir / "version_info.txt"
        if version_file.exists() and sys.platform == "win32":
            cmd.extend(["--version-file", str(version_file)])
            
        # 添加主脚本
        cmd.append("main.py")
        
        # 打印命令（用于调试）
        print(f"  执行命令: {' '.join(cmd[:5])}...")  # 只打印前几个参数
        
        try:
            # 执行打包
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                print("  ✓ 构建成功！")
                
                # 检查输出文件
                if mode == "onefile":
                    exe_path = self.dist_dir / f"{self.app_name}.exe"
                else:
                    exe_path = self.dist_dir / self.app_name / f"{self.app_name}.exe"
                    
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / 1024 / 1024
                    print(f"  ✓ 生成文件: {exe_path}")
                    print(f"  ✓ 文件大小: {size_mb:.2f} MB")
                    
                return True
            else:
                print("  ✗ 构建失败")
                print(f"\n错误输出:\n{result.stderr}")
                
                # 提供可能的解决方案
                if "No module named" in result.stderr:
                    print("\n💡 可能的解决方案:")
                    print("  1. 检查是否所有依赖都已安装")
                    print("  2. 确保在正确的虚拟环境中")
                    print("  3. 尝试重新安装 PyInstaller: pip install --upgrade --force-reinstall pyinstaller")
                    
                return False
                
        except Exception as e:
            print(f"  ✗ 构建出错: {e}")
            print("\n💡 可能的解决方案:")
            print("  1. 确保 PyInstaller 已正确安装")
            print("  2. 尝试以管理员权限运行")
            print("  3. 检查防病毒软件是否阻止了打包过程")
            return False
            
    def create_installer(self):
        """创建安装包（可选）"""
        print("\n📦 创建便携版压缩包...")
        
        # 确定输出文件名
        timestamp = datetime.now().strftime("%Y%m%d")
        zip_name = f"{self.app_name}_v{self.app_version}_{timestamp}.zip"
        zip_path = self.dist_dir / zip_name
        
        # 查找exe文件
        exe_path = self.dist_dir / f"{self.app_name}.exe"
        if not exe_path.exists():
            # 如果是文件夹模式
            exe_path = self.dist_dir / self.app_name / f"{self.app_name}.exe"
            
        if not exe_path.exists():
            print(f"  ✗ 找不到可执行文件")
            return False
            
        # 创建压缩包
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            if exe_path.parent == self.dist_dir:
                # 单文件模式
                zipf.write(exe_path, exe_path.name)
                print(f"  添加: {exe_path.name}")
            else:
                # 文件夹模式
                for file in exe_path.parent.rglob("*"):
                    if file.is_file():
                        arcname = file.relative_to(exe_path.parent.parent)
                        zipf.write(file, arcname)
                        
        print(f"  ✓ 压缩包创建成功: {zip_path}")
        print(f"  大小: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
        return True
        
    def create_shortcuts(self):
        """创建快捷方式（Windows）"""
        print("\n🔗 创建快捷方式...")
        
        if sys.platform != "win32":
            print("  ⚠️  快捷方式仅支持 Windows 系统")
            return False
            
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            
            # 桌面快捷方式
            desktop = shell.SpecialFolders("Desktop")
            shortcut_path = os.path.join(desktop, f"{self.app_description}.lnk")
            
            exe_path = self.dist_dir / f"{self.app_name}.exe"
            if not exe_path.exists():
                exe_path = self.dist_dir / self.app_name / f"{self.app_name}.exe"
                
            if not exe_path.exists():
                print("  ✗ 找不到可执行文件，无法创建快捷方式")
                return False
            
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = str(exe_path)
            shortcut.WorkingDirectory = str(exe_path.parent)
            
            ico_file = self.icons_dir / "app.ico"
            if ico_file.exists():
                shortcut.IconLocation = str(ico_file)
            else:
                shortcut.IconLocation = str(exe_path)
                
            shortcut.Description = self.app_description
            shortcut.save()
            
            print(f"  ✓ 桌面快捷方式创建成功")
            return True
            
        except ImportError:
            print("  ⚠️  需要 pywin32 来创建快捷方式")
            print("  运行: pip install pywin32")
            return False
        except Exception as e:
            print(f"  ⚠️  创建快捷方式失败: {e}")
            return False
            
    def run(self, mode="onefile", create_zip=True, create_shortcut=False):
        """运行完整的打包流程"""
        print(f"""
╔══════════════════════════════════════════╗
║     小红书 Markdown 编辑器 - 打包工具      ║
║            Version {self.app_version}              ║
╚══════════════════════════════════════════╝
        """)
        
        # 1. 清理
        self.clean_build()
        
        # 2. 检查依赖
        if not self.check_requirements():
            print("\n❌ 请先安装缺失的依赖包")
            return False
            
        # 3. 验证主脚本
        if not self.verify_main_script():
            print("\n❌ 主脚本验证失败")
            return False
            
        # 4. 创建图标
        self.create_icon()
        
        # 5. 构建exe
        if not self.build_exe(mode):
            print("\n❌ 构建失败")
            return False
            
        # 6. 创建压缩包
        if create_zip:
            self.create_installer()
            
        # 7. 创建快捷方式
        if create_shortcut and sys.platform == "win32":
            self.create_shortcuts()
            
        # 完成
        print(f"""
╔══════════════════════════════════════════╗
║              ✅ 打包完成！                ║
╚══════════════════════════════════════════╝

📁 输出目录: {self.dist_dir}
📄 可执行文件: {self.app_name}.exe

运行方式:
  1. 直接双击 {self.app_name}.exe
  2. 或从命令行运行: .\\dist\\{self.app_name}.exe

提示:
  - 首次运行可能需要几秒钟加载
  - 确保系统已安装 Microsoft Visual C++ Redistributable
  - 如遇到问题，请查看构建日志
        """)
        
        return True

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="小红书 Markdown 编辑器打包工具")
    parser.add_argument(
        "--mode", 
        choices=["onefile", "onedir"], 
        default="onefile",
        help="打包模式: onefile=单文件, onedir=文件夹"
    )
    parser.add_argument(
        "--no-zip",
        action="store_true",
        help="不创建压缩包"
    )
    parser.add_argument(
        "--shortcut",
        action="store_true", 
        help="创建桌面快捷方式"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="显示详细调试信息"
    )
    
    args = parser.parse_args()
    
    # 如果开启调试模式
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # 创建打包器
    builder = AppBuilder()
    
    # 运行打包
    success = builder.run(
        mode=args.mode,
        create_zip=not args.no_zip,
        create_shortcut=args.shortcut
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()