import re
import sys
import os
import shutil
from urllib.parse import urlparse

IMG_NEEDLE_TYPE_MD = 1
IMG_NEEDLE_TYPE_HTML = 2


class MdImageReplacer(object):

    def __init__(self, md_file_path):
        self.typora_root = None
        if not os.path.exists(md_file_path):
            raise RuntimeError('No such file')
        self.src_md_file_path = md_file_path
        with open(md_file_path, "rb") as f:
            self.content = f.read().decode()
            m = re.match(r".*typora-root-url:(.*?)\n.*", self.content,
                         re.DOTALL)
            if m:
                raw_typora_root = m.groups()[0].strip().replace('\\', '/')
                self.typora_root = os.path.join(
                    os.path.dirname(self.src_md_file_path), raw_typora_root)
                self.typora_root = os.path.abspath(self.typora_root)

    def find_all_picture_needles(self):
        ret = []
        # 匹配 Markdown 图片
        pattern = r"(!\[([^\[\]]*)\]\s*\(([^\)]*)\))"
        image_list = re.findall(pattern, self.content)
        for needle, name, location in image_list:
            ret.append((IMG_NEEDLE_TYPE_MD, needle, name, location, None))

        # 匹配 HTML 图片
        pattern = r'(<img src="([^"]*)" alt="([^"]*)" style="([^"]*)" />)'
        image_list = re.findall(pattern, self.content)
        for needle, location, name, style in image_list:
            ret.append((IMG_NEEDLE_TYPE_HTML, needle, name, location, style))

        return ret

    def get_image_real_path(self, image_path):
        # 如果原始文件路径没有文件，有几种情况：
        #  - 已经操作过的文件
        if os.path.exists(image_path):
            return os.path.abspath(image_path)

        #  - 文件路径是相对路径(相对与源文件)
        tmp_path = os.path.join(os.path.dirname(self.src_md_file_path),
                                image_path.strip('/'))
        if os.path.exists(tmp_path):
            return os.path.abspath(tmp_path)

        #  - 文件路径是相对路径(相对于typora-root-url)
        if self.typora_root:
            tmp_path = os.path.join(self.typora_root, image_path.strip('/'))
            if os.path.exists(tmp_path):
                return tmp_path

        #  - 文件就是不存在
        return None

    def calc_replacement(self,
                         image_type,
                         name,
                         image_path,
                         dst_base_dir,
                         dst_relative_dir,
                         style=None):
        image_abs_path = self.get_image_real_path(image_path)
        if image_abs_path is None:
            return None

        if name:
            ext = os.path.splitext(image_abs_path)
            image_filename = name + ext[-1]
        else:
            image_filename = os.path.basename(image_abs_path)

        print(dst_base_dir, dst_relative_dir)
        image_dst_rel_path = os.path.join(dst_relative_dir, image_filename)
        image_dst_abs_path = os.path.join(dst_base_dir, image_dst_rel_path)
        print(f"cp {image_abs_path} {image_dst_abs_path}")
        shutil.copyfile(image_abs_path, image_dst_abs_path)

        if image_type == IMG_NEEDLE_TYPE_MD:
            return f"![{name}](/{image_dst_rel_path})"
        elif image_type == IMG_NEEDLE_TYPE_HTML:
            return f'<img src="/{image_dst_rel_path}" alt="{name}" style="{style}" />'

    def replace_pictures(self, image_base_dir, image_relative_dir):
        assert (os.path.isabs(image_base_dir))
        assert (not os.path.isabs(image_relative_dir))
        assert (os.path.exists(os.path.join(image_base_dir,
                                            image_relative_dir)))
        records = self.find_all_picture_needles()
        ret = []
        for image_type, needle, name, location, style in records:
            replacement = self.calc_replacement(image_type, name, location,
                                                image_base_dir,
                                                image_relative_dir, style)
            if replacement is None:
                continue
            ret.append((needle, replacement))

        content = self.content
        for needle, replacement in ret:
            content = content.replace(needle, replacement)
        return content

    def dump(self, md_file_path, image_base_dir, image_relative_dir):
        if not os.path.isabs(image_base_dir):
            raise RuntimeError("image_base_dir must be a absolute path")
        if os.path.isabs(image_relative_dir):
            raise RuntimeError("image_relative_dir must be a relative path")
        image_dir = os.path.join(image_base_dir, image_relative_dir)
        if not os.path.exists(image_dir):
            os.mkdir(image_dir)

        with open(md_file_path, 'wb') as f:
            f.write(
                self.replace_pictures(image_base_dir,
                                      image_relative_dir).encode())


def usage():
    print(f"Usage:")
    print(
        f"    python3 {sys.argv[0]} src_filename dst_filename image_base_absolute_dir image_relative_dir\n"
    )


def main():
    if len(sys.argv) < 5:
        usage()
        exit()
    src_filename = sys.argv[1]
    if not os.stat(src_filename):
        raise RuntimeError("No source file.")

    dst_filename = sys.argv[2]
    try:
        os.stat(dst_filename)
        overwrite = input("destination file exist, overwrite it? [Y/n]").lower()
        if overwrite == 'n':
            raise RuntimeError("Stop replacement")
        elif overwrite and overwrite != 'y':
            raise RuntimeError("Invalid input")
    except:
        pass

    image_base_abs_dir = sys.argv[3]
    try:
        image_base_abs_dir = os.path.abspath(image_base_abs_dir)
    except:
        raise RuntimeError("Image directory error.")

    image_relative_dir = sys.argv[4]

    mip = MdImageReplacer(src_filename)
    mip.dump(dst_filename, image_base_abs_dir, image_relative_dir)
    print(os.path.relpath(image_base_abs_dir, os.path.dirname(dst_filename)))


# PYTHONPATH=$PWD python -m replace_pictures \
#   /Users/root/Blog/content/cn/log/2021-09-02-grpc-cpp-tricks.new.md \
#   /Users/root/Blog/content/cn/log/2021-09-02-grpc-cpp-tricks.md \
#   /Users/root/Blog/static/ images/grpc-cpp-tricks
if __name__ == '__main__':
    main()
