import json
import ruclip
import torch
class OurModel(torch.nn.Module):

    def __init__(self, ruclip_model, ruclip_processor, clfs, device="cpu",bs=4):
        super(OurModel, self).__init__()
        self.RuClip = ruclip_model.to(device)
        self.RuClipProcessor = ruclip_processor
        self.bs = bs
        self.device = device
        self.predictor = ruclip.Predictor(self.RuClip, self.RuClipProcessor, device, bs=bs)
        self.clfNN = clfs['NN']
        self.clfYar = clfs['Yaroslavl']
        self.clfEKB = clfs['EKB']
        self.clfVl = clfs['Vladimir']
        with open("./uniq_showplaces.json") as f:
            self.showplaces_maping = json.load(f)

    def forward(self, city_name, images=None, texts=None):
        if images is None and texts is None:
            raise Exception("no data was sent")
        if images is not None:
            latent_data = self.predictor.get_image_latents(images)
        elif texts is not None:
            latent_data = self.predictor.get_text_latents(texts)
        if city_name == "Нижний Новгород":
            showplace_name = self.clfNN.predict_proba(latent_data.cpu().detach())
        elif city_name == "Ярославль":
            showplace_name = self.clfYar.predict_proba(latent_data.cpu().detach())
        elif city_name == "Екатеринбург":
            showplace_name = self.clfEKB.predict_proba(latent_data.cpu().detach())
        elif city_name == "Владивосток":
            showplace_name = self.clfVl.predict_proba(latent_data.cpu().detach())
        return torch.topk(torch.tensor(showplace_name), k=5)


if __name__ == "__main__":
    model, processor = ruclip.load("ruclip-vit-base-patch16-384", device="cpu")
    clf3 = torch.load("./clf_nn.pth")
    our_model = OurModel(model, processor, clfNN=clf3, bs=4)
    res = our_model('Нижний Новгород', texts=['ленин'])
    print(res.values[0], (our_model.showplaces_maping['NN'][res.indices[0][0].item()]))