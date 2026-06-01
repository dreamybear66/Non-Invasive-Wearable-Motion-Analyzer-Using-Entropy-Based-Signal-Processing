import { useEffect } from 'react';
import gsap from 'full/gsap';

export function useGSAP(callback, dependencies = []) {
  useEffect(() => {
    // Create a context so we can easily revert all animations created inside this hook
    const ctx = gsap.context(() => {
      callback();
    });

    return () => {
      // Cleanup all animations on unmount or dependency change
      ctx.revert();
    };
  }, dependencies); // eslint-disable-line react-hooks/exhaustive-deps
}
