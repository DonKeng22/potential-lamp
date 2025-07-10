import React, { useRef, useState } from 'react';
import ReactPlayer from 'react-player/youtube';
import { Stage, Layer, Rect } from 'react-konva';

interface FieldBoundary {
  x: number;
  y: number;
  width: number;
  height: number;
  angle: number;
}

const defaultBoundary: FieldBoundary = {
  x: 100,
  y: 100,
  width: 400,
  height: 200,
  angle: 0,
};

const FieldHockeyAnnotator: React.FC = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [boundary, setBoundary] = useState<FieldBoundary>(defaultBoundary);
  const [drawing, setDrawing] = useState(false);
  const [startPos, setStartPos] = useState<{x: number, y: number} | null>(null);

  // Handle YouTube link input
  const handleUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVideoUrl(e.target.value);
  };

  // Handle drawing the field boundary
  const handleStageMouseDown = (e: any) => {
    if (!drawing) {
      const pos = e.target.getStage().getPointerPosition();
      setStartPos(pos);
      setDrawing(true);
    }
  };

  const handleStageMouseUp = (e: any) => {
    if (drawing && startPos) {
      const pos = e.target.getStage().getPointerPosition();
      setBoundary({
        x: Math.min(startPos.x, pos.x),
        y: Math.min(startPos.y, pos.y),
        width: Math.abs(pos.x - startPos.x),
        height: Math.abs(pos.y - startPos.y),
        angle: 0,
      });
      setDrawing(false);
      setStartPos(null);
    }
  };

  // Allow manual angle adjustment
  const handleAngleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBoundary({ ...boundary, angle: parseFloat(e.target.value) });
  };

  // Save annotation (stub)
  const handleSave = () => {
    // TODO: POST to backend
    alert('Annotation saved! (stub)');
  };

  // Load annotation (stub)
  const handleLoad = () => {
    // TODO: GET from backend
    setBoundary(defaultBoundary);
    alert('Annotation loaded! (stub)');
  };

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: 24 }}>
      <h2>Field Hockey Video Annotator (Prototype)</h2>
      <div style={{ marginBottom: 16 }}>
        <input
          type="url"
          placeholder="Paste YouTube link..."
          value={videoUrl}
          onChange={handleUrlChange}
          style={{ width: 400, marginRight: 8 }}
        />
      </div>
      <div style={{ display: 'flex', gap: 24 }}>
        <div>
          <ReactPlayer url={videoUrl} controls width={480} height={270} />
        </div>
        <div>
          <Stage
            width={480}
            height={270}
            style={{ border: '1px solid #ccc', background: '#eaf6e6' }}
            onMouseDown={handleStageMouseDown}
            onMouseUp={handleStageMouseUp}
          >
            <Layer>
              <Rect
                x={boundary.x}
                y={boundary.y}
                width={boundary.width}
                height={boundary.height}
                rotation={boundary.angle}
                stroke="red"
                strokeWidth={3}
                draggable
                onDragEnd={e => setBoundary({ ...boundary, x: e.target.x(), y: e.target.y() })}
                onTransformEnd={e => {
                  const node = e.target;
                  setBoundary({
                    ...boundary,
                    x: node.x(),
                    y: node.y(),
                    width: node.width() * node.scaleX(),
                    height: node.height() * node.scaleY(),
                    angle: node.rotation(),
                  });
                }}
              />
            </Layer>
          </Stage>
          <div style={{ marginTop: 8 }}>
            <label>Angle: <input type="number" value={boundary.angle} onChange={handleAngleChange} step={1} /></label>
          </div>
          <div style={{ marginTop: 8 }}>
            <button onClick={handleSave}>Save Annotation</button>
            <button onClick={handleLoad} style={{ marginLeft: 8 }}>Load Annotation</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FieldHockeyAnnotator;
