import React, { useRef, useEffect, useState } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Sphere } from '@react-three/drei';
import * as THREE from 'three';

const Sphere3D = ({ data, texture }) => {
    const meshRef = useRef();
    const [rotation, setRotation] = useState([0, 0, 0]);

    useFrame(() => {
        if (meshRef.current) {
            meshRef.current.rotation.x = rotation[0];
            meshRef.current.rotation.y = rotation[1];
            meshRef.current.rotation.z = rotation[2];
        }
    });

    return (
        <Sphere ref={meshRef} args={[1, 32, 32]}>
            <meshStandardMaterial
                map={texture}
                metalness={0.1}
                roughness={0.5}
            />
        </Sphere>
    );
};

const Scene = ({ data, texture }) => {
    return (
        <Canvas camera={{ position: [0, 0, 2.5] }}>
            <ambientLight intensity={0.5} />
            <pointLight position={[10, 10, 10]} />
            <Sphere3D data={data} texture={texture} />
            <OrbitControls enablePan={true} enableZoom={true} enableRotate={true} />
        </Canvas>
    );
};

export default Scene; 