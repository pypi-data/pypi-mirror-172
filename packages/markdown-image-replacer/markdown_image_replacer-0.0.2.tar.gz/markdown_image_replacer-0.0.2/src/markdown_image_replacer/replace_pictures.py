import re
import urllib.request
import os
import shutil

IMG_NEEDLE_TYPE_MD = 1
IMG_NEEDLE_TYPE_HTML = 2

FILE_TYPE_LOCAL = 1
FILE_TYPE_REMOTE = 2


class MdImageReplacer(object):

    def __init__(self, src_md_file, src_img_root, md_img_search_label, dst_md_file, dst_img_root, dst_img_rel_dir):
        if not os.path.exists(src_md_file):
            raise RuntimeError('No such file')
        self.src_md_file = src_md_file

        self.dst_md_file = dst_md_file
        self.dst_img_root = dst_img_root
        self.dst_img_rel_dir = dst_img_rel_dir

        if not os.path.isabs(self.dst_img_root):
            raise RuntimeError("dst_img_root must be a absolute path")
        if os.path.isabs(self.dst_img_rel_dir):
            raise RuntimeError("dst_img_rel_dir must be a relative path")

        self.dst_img_dir = os.path.join(self.dst_img_root, self.dst_img_rel_dir)
        if not os.path.exists(self.dst_img_dir):
            os.makedirs(self.dst_img_dir)

        self.src_img_root = src_img_root
        self.md_img_search_label = []

        if isinstance(md_img_search_label, str):
            self.md_img_search_label = [md_img_search_label]
        elif isinstance(md_img_search_label, list):
            self.md_img_search_label = md_img_search_label

        self.image_search_root_list = []
        f = open(self.src_md_file, "rb")
        self.content = f.read().decode()
        for label in self.md_img_search_label:
            for line in self.content.split('\n'):
                m = re.match(rf"^\s*{label}:(.*?)$", line)
                if not m:
                    continue
                image_search_root = m.groups()[0].strip().replace('\\', os.sep)
                image_search_root = os.path.join(os.path.dirname(self.src_md_file), image_search_root)
                self.image_search_root_list.append(os.path.abspath(image_search_root))
        f.close()

    def find_all_image_needles(self):
        ret = []
        # 匹配 Markdown 图片
        pattern = r"(!\[([^\[\]]*)\]\s*\(([^\)]*)\))"
        image_list = re.findall(pattern, self.content)
        for needle, alt_name, location in image_list:
            ret.append((IMG_NEEDLE_TYPE_MD, needle, alt_name, location, None))

        # 匹配 HTML 图片
        pattern = r'(<img src="([^"]*)" alt="([^"]*)" style="([^"]*)" />)'
        image_list = re.findall(pattern, self.content)
        for needle, location, alt_name, style in image_list:
            ret.append((IMG_NEEDLE_TYPE_HTML, needle, alt_name, location, style))

        return ret

    def get_image_real_path(self, image_path):
        # 如果是网络 URL 则直接返回(TODO 判断类型加扩展名)
        if image_path.find("://") >= 0:
            return FILE_TYPE_REMOTE, image_path

        # 如果原始文件路径没有文件，有几种情况：
        #  - 已经操作过的文件
        if os.path.exists(image_path):
            return FILE_TYPE_LOCAL, os.path.abspath(image_path)

        #  - 文件路径是相对路径(相对与源文件)
        tmp_path = os.path.join(os.path.dirname(self.src_md_file),
                                image_path.strip('/'))
        if os.path.exists(tmp_path):
            return FILE_TYPE_LOCAL, os.path.abspath(tmp_path)

        #  - 文件路径是相对路径(相对于静态目录)
        if self.src_img_root:
            image_path = os.path.join(self.src_img_root, image_path.strip('/'))
            if os.path.exists(image_path):
                return FILE_TYPE_LOCAL, image_path

        #  - 文件路径是相对路径(相对于 Markdown 中特定 label 指定的路径)
        for search_root in self.image_search_root_list:
            image_path = os.path.join(search_root, image_path.strip('/'))
            if os.path.exists(image_path):
                return FILE_TYPE_LOCAL, image_path

        #  - 文件就是不存在
        return None, None

    def calc_replacement(self, records):
        needle_replacement_list = []
        for image_type, needle, alt_name, image_path, style in records:
            file_type, image_abs_path = self.get_image_real_path(image_path)
            print("!!", image_path, file_type)
            if file_type is None:
                continue

            if alt_name:
                ext = os.path.splitext(image_abs_path)
                image_filename = alt_name + ext[-1]
            else:
                image_filename = os.path.basename(image_abs_path)

            image_dst_rel_path = os.path.join(self.dst_img_rel_dir, image_filename)
            image_dst_abs_path = os.path.join(self.dst_img_root, image_dst_rel_path)

            if file_type == FILE_TYPE_REMOTE:  # http/https/ftp
                # download file to image_dst_abs_path
                print(f"store to {image_dst_abs_path} by downloading {image_abs_path}")
                urllib.request.urlretrieve(image_abs_path, image_dst_abs_path)
                pass
            else:  # local
                print(f"cp {image_abs_path} {image_dst_abs_path}")
                shutil.copyfile(image_abs_path, image_dst_abs_path)

            if image_type == IMG_NEEDLE_TYPE_MD:
                replacement = f"![{alt_name}](/{image_dst_rel_path})"
            elif image_type == IMG_NEEDLE_TYPE_HTML:
                replacement = f'<img src="/{image_dst_rel_path}" alt="{alt_name}" style="{style}" />'

            needle_replacement_list.append((needle, replacement))
        return needle_replacement_list

    def process(self):
        records = self.find_all_image_needles()
        print(records)
        needle_replacement_list = self.calc_replacement(records)

        content = self.content
        for needle, replacement in needle_replacement_list:
            content = content.replace(needle, replacement)

        with open(self.dst_md_file, 'wb') as f:
            f.write(content.encode())
