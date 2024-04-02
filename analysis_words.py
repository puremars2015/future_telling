from emodic import emodic
try:
    import jieba
except:
    import os
    os.system('pip install jieba')
    import jieba

def ValidateTheEmoGrade(text: str):
    pos_score = 0
    pos = []
    neg_score = 0
    neg = []
    dic = emodic()
    jieba_result = jieba.cut(text,cut_all=False,HMM=True)
    for word in jieba_result:
        if word in dic.PositiveDict():
            pos_score += 1
            pos.append(word)
        elif word in dic.NegativeDict():
            neg_score += 1
            neg.append(word)
        else:
            pass
    return pos_score - neg_score

def ShowEmoWords(text: str):
    pos_score = 0
    pos = []
    neg_score = 0
    neg = []
    dic = emodic()
    jieba_result = jieba.cut(text,cut_all=False,HMM=True)
    for word in jieba_result:
        if word in dic.PositiveDict():
            pos.append(word)
        elif word in dic.NegativeDict():
            neg.append(word)
        else:
            pass
    return ((pos_score, pos),(neg_score,neg))


# grade = ValidateTheEmoGrade('''〔記者王孟倫／台北報導〕近日傳出，有國內保經公司業務員違法銷售、未經金管會核准或備查的保單商品（俗稱境外保單或地下保單），而遭到地檢署偵查，將該名業務員依違反保險法起訴。金管會強調，凡違法銷售境外地下保單，依法可處3年以下有期徒刑，得併科300萬元以上、2千萬元以下罰金。
# 為保障我國金融消費者權益，金管會表示，凡未規定向主管機關申請核准的保單商品，就是違法銷售行為；若國內公司代為銷售這些境外地下保單，亦屬違法行為。
# 如果替非保險法之保險業或外國保險業代理、經紀或招攬保險業務者，處3年以下有期徒刑，得併科新臺幣3百萬元以上2千萬元以下罰金；情節重大者，得由主管機關對保險代理人、經紀人、公證人或兼營保險代理人或保險經紀人業務之銀行停止一部或全部業務，或廢止許可，並註銷執業證照。
# 金管會提醒消費者，這類境外保單有四大風險，包括：第一、法律管轄問題：這類從境外簽發的保單，有些的確是在國際知名的大保險公司，問題是，這些保險公司的註冊地在海外，不受台灣保險法令規範，也就是說，金管會無法協助及維護消費者的權益。
# 第二、發生理賠、保全服務等問題：因為發行境外保單的保險公司在台灣並沒有據點，一旦出險，保戶需自行接洽遠在海外的業者，未來難以獲完整服務及保障；尤其，這類境外保單屬於地下保單，其保戶應有權益不在保險安定基金保障範圍；也就是說，公司若倒閉，保戶將血本無歸。
# 第三、境外保單契約多以英文書寫：密密麻麻的保險契約條文，消費者不易理解保單相關的權利、義務，可能出現對契約內容認知的差距，進而產生投保爭議，保戶可能要自行打越洋官司。
# 第四，國內法律適用問題：境外保單就是一種地下保單，並不被國內法律所承認，因此，投保地下保單所支付的保費，既無法做為所得稅列舉扣除額，且地下保單的死亡保險金、即使已指定受益人，也不適用保險法有關死亡給付不得作為被保險人遺產規定，也就是「不享有保單死亡給付免稅的優惠」。
# 對於違法銷售境外保單，金管會呼籲切勿以身試法，民眾若有發現招攬境外保單的具體事證，可檢證向司法單位告發，或送金管會協助處理檢舉事宜。
# ''')

# print(grade)

# txt = '''根據以上文章的內容來看，整體情緒呈現悲觀，對股市未來狀況的影響可能被認為是負面的。文章著重強調了違法銷售境外保單的嚴重性，並列舉了四大風險，包括法律管轄問題、理賠保全服務問題、保單契約書寫問題以及國內法律適用問題。這些風險的存在可能會對金融消費者的權益造成威脅，並對整體市場信心帶來負面影響。金管會的告誡和呼籲也顯示了這個議題的嚴肅性和可能對市場帶來的影響。因此, 這篇文章對股市未來狀況的情緒可以說是悲觀的。'''

# print(ValidateTheEmoGrade(txt))

# print(ShowEmoWords(txt))