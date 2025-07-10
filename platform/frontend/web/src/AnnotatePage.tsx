import React, { useRef, useState } from 'react';
import ReactPlayer from 'react-player/youtube';
import { Stage, Layer, Rect, Transformer } from 'react-konva';

// Minimal annotation type
interface FieldBoundary {
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: number;
}

const defaultBoundary: FieldBoundary = {
  x: 100,
  y: 100,
  width: 400,
  height: 200,
  rotation: 0,
};

const AnnotatePage = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [boundary, setBoundary] = useState<FieldBoundary>(defaultBoundary);
  const [selected, setSelected] = useState(false);
  const trRef = useRef<any>(null);
  const rectRef = useRef<any>(null);

  // Save annotation (stub)
  const handleSave = () => {
    // TODO: POST to backend
    alert('Saved! ' + JSON.stringify(boundary));
  };

  // Load annotation (stub)
  const handleLoad = () => {
    // TODO: GET from backend
    setBoundary(defaultBoundary);
  };

  return (
    <div style={{ padding: 32, maxWidth: 900, margin: '0 auto' }}>
      <h1>Field Hockey Annotation Tool (Minimal Prototype)</h1>
      <div style={{ marginBottom: 16 }}>
        <input
          type="url"
          placeholder="Paste YouTube link..."
          value={videoUrl}
          onChange={e => setVideoUrl(e.target.value)}
          style={{ width: 400, padding: 8 }}
        />
      </div>
      {videoUrl && (
        <div style={{ marginBottom: 16 }}>
          <ReactPlayer url={videoUrl} controls width={640} height={360} />
        </div>
      )}
      <div style={{ border: '1px solid #ccc', width: 640, height: 360, marginBottom: 16, position: 'relative' }}>
        <Stage width={640} height={360}>
          <Layer>
            <Rect
              ref={rectRef}
              x={boundary.x}
              y={boundary.y}
              width={boundary.width}
              height={boundary.height}
              rotation={boundary.rotation}
              fill="rgba(0,255,0,0.1)"
              stroke="green"
              strokeWidth={2}
              draggable
              onClick={() => setSelected(true)}
              onTap={() => setSelected(true)}
              onDragEnd={e => setBoundary({ ...boundary, x: e.target.x(), y: e.target.y() })}
              onTransformEnd={e => {
                const node = rectRef.current;
                setBoundary({
                  ...boundary,
                  x: node.x(),
                  y: node.y(),
                  width: node.width() * node.scaleX(),
                  height: node.height() * node.scaleY(),
                  rotation: node.rotation(),
                });
                node.scaleX(1);
                node.scaleY(1);
              }}
            />
            {selected && (
              <Transformer
                ref={trRef}
                nodes={[rectRef.current]}
                rotateEnabled={true}
                enabledAnchors={['top-left', 'top-right', 'bottom-left', 'bottom-right']}
              />
            )}
          </Layer>
        </Stage>
      </div>
      <button onClick={handleSave} style={{ marginRight: 8 }}>Save Annotation</button>
      <button onClick={handleLoad}>Load Annotation</button>
    </div>
  );
};

export default AnnotatePage;
