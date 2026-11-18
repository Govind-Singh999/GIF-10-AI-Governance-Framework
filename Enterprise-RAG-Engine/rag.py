import argparse, json, math, re
from pathlib import Path
from collections import Counter
from dataclasses import dataclass
STOP=set('a an the is are was were of to for in on at and or do does what when how which who we our it be can should with from'.split())
def tokens(text): return [t for t in re.findall(r'[a-z0-9]+',text.lower()) if t not in STOP]
@dataclass(frozen=True)
class Chunk:
    source:str
    paragraph:int
    text:str

def load(folder):
    out=[]
    for p in sorted(Path(folder).glob('*.txt')):
        if p.is_symlink(): continue
        for i,t in enumerate(re.split(r'\n\s*\n',p.read_text(encoding='utf8')),1):
            if t.strip(): out.append(Chunk(p.name,i,t.strip()))
    return out

class Index:
    def __init__(self,chunks):
        self.chunks=list(chunks); self.counts=[Counter(tokens(c.text)) for c in self.chunks]
        self.lengths=[sum(c.values()) for c in self.counts]
        self.avg=sum(self.lengths)/len(self.lengths) if self.lengths else 1
        self.df=Counter(w for c in self.counts for w in c)
    def search(self,question,k=3):
        q=set(tokens(question)); n=len(self.chunks); ranked=[]
        for i,c in enumerate(self.chunks):
            score=0.; matches=q & self.counts[i].keys()
            for w in matches:
                df=self.df[w]; tf=self.counts[i][w]; idf=math.log(1+(n-df+.5)/(df+.5))
                denom=tf+1.5*(.25+.75*self.lengths[i]/max(self.avg,1e-9))
                score+=idf*tf*2.5/denom
            coverage=len(matches)/len(q) if q else 0
            if score>0: ranked.append((score,coverage,c))
        return sorted(ranked,key=lambda x:(-x[0],x[2].source,x[2].paragraph))[:max(0,k)]
    def answer(self,question):
        hits=self.search(question)
        if not hits or hits[0][0]<.25 or hits[0][1]<.5:
            return {'status':'insufficient_evidence','evidence':[]}
        return {'status':'evidence_found','evidence':[{'source':c.source,'paragraph':c.paragraph,'excerpt':c.text,'score':round(s,4)} for s,coverage,c in hits if coverage>=.5]}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('question'); a=p.parse_args()
    print(json.dumps(Index(load(a.folder)).answer(a.question),indent=2))
