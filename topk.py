import ruclip
import argparse
import numpy as np
import torch
import pickle
import PIL


class TopK:
    def __init__(self, bas=8, path_ruclip='ruclip-vit-base-patch16-384', path_cls='clf.pth'):
        self.model, self.processor = ruclip.load(path_ruclip, device='cpu')
        self.cls = pickle.load(open(path_cls, 'rb'))
        self.predictor = ruclip.predictor(self.model, self.processor, 'cpu', bs=bas)

    def get_by_im(self, imgs, hm):
        with torch.no_grad():
            emb = self.predictor.get_image_latents(imgs)
            y_pred = self.cls.predict_proba(emb.cpu().detach())
            y = torch.tensor(y_pred)
            topk = torch.topk(y, k=hm)
            return topk

    def get_by_text(self, texts, hm):
        with torch.no_grad():
            emb = self.predictor.get_image_latents(texts)
            y_pred = self.cls.predict_proba(emb.cpu().detach())
            y = torch.tensor(y_pred)
            topk = torch.topk(y, k=hm)
            return topk


def main(arg):
    model = TopK(8, path_cls=arg.cls)
    if arg.text == 0:
        img = PIL.Image.open(arg.path)
        res = model.get_by_im(img, arg.topk)
    else:
        res = model.get_by_text(arg.input, arg.topk)
    torch.save(res, arg.outpath)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topk', type=int, default=5, help='How many classes should i predict')
    parser.add_argument('--text', type=int, default=0, help='top on description, on img otherwise')
    parser.add_argument('--cls', type=str, default=None, help='classificator path')
    parser.add_argument('--input', type=str, default=None, help='path to file')
    parser.add_argument('--outpath', type=str, default=None, help='path to out')
    args = parser.parse_args()
    main(args)