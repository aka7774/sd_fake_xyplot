# sd_fake_xyplot
Generate X/Y Plot-like images.

これが

![input](doc/input.png)

こうや

![output](doc/output.png)

画像はstable-diffusion-webui直下からの相対パスやでー

これは

![output](doc/rank.png)

Zだと横が先
```
12
34
56
```

Nだと縦が先
```
14
25
36
```

X,Yに対して画像が足りないとエラー

画像が余ってるぶんは無視する
