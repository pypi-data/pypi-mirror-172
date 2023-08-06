from subprocess import run, PIPE
import requests
import pysubs2
import json
import os
import re


pkg_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pkg_data")
pkg_data = os.path.join(pkg_data_dir, "data.json")


class SVO:
    data = json.loads(open(pkg_data, "rb").read().decode())
    ffmpeg_bin = None

    def __init__(
            self,
            language, # type: str
            gender = None, # type: str
            speed = 100, # type: int
            volume = 0, # type: int
            pause = 0.2, # type: float
            voice = None # type: str
    ):
        if not gender and not voice:
            raise ValueError("please specify gender or voice")
        self.language = language
        self.gender = gender
        self.voice = voice
        self.speed = speed
        self.volume = volume
        self.pause = pause
        self.voices = []
        if self.gender:
            for k, v in self.data.items():
                if v["languageCode"] == self.language and v["gender"] == self.gender:
                    self.voices.append(v)
            self.voices.sort(key=lambda v: [v["service"], v["name"]])

    @property
    def languageCode(self, seen = []):
        if seen:
            return seen
        for k, v in self.data.items():
            lc = v["languageCode"]
            if lc not in seen:
                seen.append(lc)
        seen.sort()
        return seen

    def tts(
            self,
            text, # type: str
            speed = 100, # type: int
            volume = 0, # type: int
            pause = 0, # type: int
            voice = None, # type: str
            fp = None # type: str
    ):
        speed = speed or self.speed
        volume = volume or self.volume
        pause = pause or self.pause
        voice = voice or self.voice
        if not voice:
            m = [
                len(max([_["value"] for _ in self.voices], key=len)),
                len(max([_["name"] for _ in self.voices], key=len)),
                len(max([_["service"] for _ in self.voices], key=len)),
            ]
            template = "{{:<{}}}\t{{:<{}}}\t{{:<{}}}".format(*m)
            print(template.format("value", "name", "service"))
            print(template.format("", "", "").replace(" ", "-"))
            for v in self.voices:
                print(template.format(v["value"], v["name"], v["service"]))
            voice = input("input voice (value): ")
        if pause:
            text = re.sub("(\r\n|\r|\n|[.,!?。，！？])", "\g<1><break time=\"{}s\"/>".format(pause), text)
            # print(text)
            # return
        params = {
            "globalSpeed": str(speed) + "%",
            "globalVolume": ("+" if volume >= 0 else "") + str(volume) + "dB",
            "chunk": "<speak><p>" + text + "</p></speak>",
            "narrationStyle": "regular",
            "platform": "landing_demo",
            "ssml": "<speak><p>" + text + "</p></speak>",
            "userId": "5pe8l4FrdbczcoHOBkUtp0W37Gh2",
            "voice": voice
        }
        r = requests.post("https://play.ht/api/transcribe", data=params)
        if "audio" in r.headers["Content-Type"]:
            c = r.content
        else:
            c = requests.get(r.json()["file"]).content
        if fp:
            open(fp, "wb").write(c)
            return fp
        return c

    def ffmpeg(self, cmd):
        return run([self.ffmpeg_bin]+list(map(str, cmd)), stdout=PIPE, stderr=PIPE)

    def generate(
            self,
            fp,
            out = None, # type: str
            **kwargs
    ):
        if not self.ffmpeg_bin:
            raise Exception("please set ffmpeg_bin first")
        if isinstance(fp, str) and os.path.isfile(fp):
            texts = open(fp, "rb").read().decode()
            if not out:
                out = fp+"{}.mp3"
        elif hasattr(fp, "read"):
            texts = fp.read()
            try:
                texts = texts.decode()
            except:
                pass
        else:
            texts = fp
        es = pysubs2.ssafile.SSAFile.from_string(texts).events
        texts = None
        s = es[-1].end/1000
        cmd = ["-f", "lavfi", "-t", s, "-i", "color=c=black:s=100x100", "-f", "lavfi", "-t", s, "-i", "anullsrc=channel_layout=stereo:sample_rate=48000", "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p", "-y", "tmp.mp4"]
        (self.ffmpeg(cmd))
        rs = []
        cmd = ["-i", "tmp.mp4"]
        suffix = ["-map", "0:0", "-map", "0:1"]
        for i, e in enumerate(es):
            fp = out.format(".{:0>5}".format(i)) if "{}" in out else out
            cmd.extend(["-itsoffset", e.start/1000, "-i", fp])
            suffix.extend(["-map", "{}:0".format(i+1)])
            text = e.plaintext.strip()
            self.tts(
                text=text,
                fp=fp,
                **kwargs
            )
            rs.append(fp)
        out = out.format("") if "{}" in out else out
        cmd = cmd+suffix+["-async", "1", "-y", out+".mp4"]
        (self.ffmpeg(cmd))
        cmd = ["-i", out+".mp4", "-filter_complex", "[0:a]amix=inputs=3[a]", "-ac", "2", "-map", "0:0", "-map", "[a]", "-c:v", "copy", "-async", "1", "-y", out+".2.mp4"]
        (self.ffmpeg(cmd))
        cmd = ["-i", out+".2.mp4", "-c:a", "libmp3lame", "-async", "1", "-y", out]
        (self.ffmpeg(cmd))
        try:
            os.remove("tmp.mp4")
            os.remove(out+".2.mp4")
            os.remove(out+".mp4")
            list(map(os.remove, rs))
        except:
            pass
        return out




