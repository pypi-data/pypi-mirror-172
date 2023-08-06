import os
import argparse
from .replace_pictures import MdImageReplacer


def main():
    parser = argparse.ArgumentParser(
        description='Process markdown by replacing images path with copied or downloaded ones')
    parser.add_argument('src_md_file', metavar='src_md_file', type=str, help='source markdown file to process')
    parser.add_argument('--src_img_root', type=str)
    parser.add_argument('--md_img_search_label', type=str, default="typora-root-url",
                        help="base path in markdown marked by label, default \"typora-root-url\"")
    parser.add_argument('--dst_md_file', type=str)
    parser.add_argument('--dst_img_root', type=str, required=True)
    parser.add_argument('--dst_img_rel_dir', type=str, required=True)

    args = parser.parse_args()
    # args = parser.parse_args([
    #     "/Users/panzhongxian/hugo/quickstart/content/posts/my-first-post.md",
    #     "--src_img_root", "/Users/panzhongxian/hugo/quickstart/static",
    #     "--dst_md_file", "/Users/panzhongxian/hugo/quickstart/content/posts/my-first-post2.md",
    #     "--dst_img_root", "/Users/panzhongxian/hugo/quickstart/static",
    #     "--dst_img_rel_dir", "images/my-first-post",
    # ])

    if not os.stat(args.src_md_file):
        raise RuntimeError("No source file.")

    if args.dst_md_file is None:
        args.dst_md_file = args.src_md_file

    if args.src_img_root is None:
        args.src_img_root = args.dst_img_root

    try:
        os.stat(args.dst_md_file)
        overwrite = input("destination file exist, overwrite it? [Y/n]").lower()
        if overwrite == 'n':
            raise RuntimeError("Stop replacement")
        elif overwrite and overwrite != 'y':
            raise RuntimeError("Invalid input")
    except:
        pass

    try:
        os.path.abspath(args.dst_img_rel_dir)
    except:
        raise RuntimeError("Image directory error.")

    mip = MdImageReplacer(args.src_md_file, args.src_img_root, args.md_img_search_label, args.dst_md_file,
                          args.dst_img_root, args.dst_img_rel_dir)
    mip.process()
    print(os.path.relpath(args.dst_img_root, os.path.dirname(args.dst_md_file)))


main()
