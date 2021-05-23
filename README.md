# CCTV Facedetection - Telegram Bot

## Create MJPEG Stream Camera
- follow this tutorial (https://yunusmuhammad007.medium.com/membuat-mjpeg-stream-camera-menggunakan-esp32-cam-part-1-e18fd0f37080)

## Create Bot 
1. Create a new bot using 'BotFather' on Telegram. Reference https://core.telegram.org/bots. BotFather supplies a TOKEN for your new bot. 
2. Go to https://web.telegram.org,
3. Create New Group and add your Bot to that group,
4. Find your link (URL) of Group like (https://web.telegram.org/#/im?p=g123456789)
5. Copy that number after `g` and put a (`-`) before that `-123456789`
6. `-123456789` is your CHAT ID

## Build your own Image
1. Clonne this repository
```
mkdir Github
cd Github
git clone https://github.com/Muhammad-Yunus/cctv_facedetection_telegram.git

```
2. Docker build,
```
docker build --pull --rm -f "cctv_facedetection_telegram/Dockerfile" -t cctv_facedetect_telegram_bot:latest "cctv_facedetection_telegram"
```
3. Docker Run,
```
docker run --rm -d --name cctv_facedetect_telegram_bot  -p 8083:8083/tcp \
-e BOT_TOKEN='xxxxxxxxxxxxxxxxx' \
-e CHAT_ID='xxxxxxxx' \
-e MJPEG_URL="https://IP:PORT/MY_MJPEG_URL/" \
-e "TZ=Asia/Jakarta" \
cctv_facedetect_telegram_bot:latest
``` 

## Or, Pull image & run from my Docker Registry (Docker Hub)
1. Pull & Run Image,
```
docker run --rm -d --name cctv_facedetect_telegram_bot  -p 8083:8083/tcp \
-e BOT_TOKEN='xxxxxxxxxxxxxxxxx' \
-e CHAT_ID='xxxxxxxx' \
-e MJPEG_URL="https://IP:PORT/MY_MJPEG_URL/" \
-e "TZ=Asia/Jakarta" \
yunusdev/cctv_facedetect_telegram_bot:latest
```