const BASE_URL = "/api/train";

export async function startTraining(videoLink: string) {
  const res = await fetch(`${BASE_URL}/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ video_link: videoLink })
  });
  return res.json();
}

export async function fetchAnnotations() {
  const res = await fetch(`${BASE_URL}/annotations`);
  return res.json();
}

export async function fetchInsights() {
  const res = await fetch(`${BASE_URL}/insights`);
  return res.json();
}
