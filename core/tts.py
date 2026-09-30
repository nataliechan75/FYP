"""
Edge TTS：用 Microsoft Neural voice 生成粵語 MP3
"""
import asyncio
import edge_tts


YUE_VOICES = {
    "female_1": "zh-HK-HiuMaanNeural",
    "female_2": "zh-HK-HiuGaaiNeural",
    "male_1": "zh-HK-WanLungNeural",
}


async def _generate_async(text: str, voice: str, rate: str = "-10%") -> bytes:
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data


def generate_speech(text: str, voice_key: str = "female_1", rate: str = "-10%") -> bytes:
    voice = YUE_VOICES.get(voice_key, YUE_VOICES["female_1"])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_generate_async(text, voice, rate))
    finally:
        loop.close()
