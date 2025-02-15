Shader "Unlit/HeatmapShader"
{
  Properties
  {
    _MainTex("Texture", 2D) = "white" {}
      _Color0("Color 0", Color) = (1, 1, 1, 1)
      _Color1("Color 1",Color) = (0,.9,.2,1)
      _Color2("Color 2",Color) = (.9,1,.3,1)
      _Color3("Color 3",Color) = (.9,.7,.1,1)
      _Color4("Color 4",Color) = (1,0,0,1)

      _Range0("Range 0",Range(0,1)) = 0.
      _Range1("Range 1",Range(0,1)) = 0.25
      _Range2("Range 2",Range(0,1)) = 0.5
      _Range3("Range 3",Range(0,1)) = 0.75
      _Range4("Range 4",Range(0,1)) = 1

      _Diameter("Diameter",Range(0,1)) = 1.0
      _Strength("Strength",Range(.1,4)) = 1.0
      _PulseSpeed("Pulse Speed",Range(0,5)) = 0
  }
    SubShader
    {
      Tags { "Queue"="Transparent" "IgnoreProjector"="True" "RenderType"="Transparent"  }
      LOD 100

      ZWrite Off
      Lighting Off
      Fog { Mode Off }
      Blend SrcAlpha OneMinusSrcAlpha 
        
      Pass
      {
        CGPROGRAM
        #pragma vertex vert
        #pragma fragment frag
        #pragma multi_compile_fog

        #include "UnityCG.cginc"

        struct appdata
        {
          float4 vertex : POSITION;
          float2 uv : TEXCOORD0;
        };

        struct v2f
        {
          float2 uv : TEXCOORD0;
          UNITY_FOG_COORDS(1)
          float4 vertex : SV_POSITION;
        };

        sampler2D _MainTex;
        float4 _MainTex_ST;

        float4 _Color0;
        float4 _Color1;
        float4 _Color2;
        float4 _Color3;
        float4 _Color4;


        float _Range0;
        float _Range1;
        float _Range2;
        float _Range3;
        float _Range4;
        float _Diameter;
        float _Strength;

        float _PulseSpeed;

        v2f vert(appdata v)
        {
          v2f o;
          o.vertex = UnityObjectToClipPos(v.vertex);
          o.uv = TRANSFORM_TEX(v.uv, _MainTex);
          UNITY_TRANSFER_FOG(o,o.vertex);
          return o;
        }
        //----

        float4 colors[5]; //colors for point ranges
        float pointranges[5];  //ranges of values used to determine color values
        float _Hits[3 * 32]; //passed in array of pointranges 3floats/point, x,y,intensity
        int _HitCount = 0;
        float _circleDiameter= 0.0;
        void initalize()
        {
          colors[0] = _Color0;
          colors[1] = _Color1;
          colors[2] = _Color2;
          colors[3] = _Color3;
          colors[4] = _Color4;
          pointranges[0] = _Range0;
          pointranges[1] = _Range1;
          pointranges[2] = _Range2;
          pointranges[3] = _Range3;
          pointranges[4] = _Range4;
        }

        float4 getHeatForPixel(float weight)
        {
          if (weight <= pointranges[0])
          {
            return colors[0];
          }
          if (weight >= pointranges[4])
          {
            return colors[4];
          }
          for (int i = 1; i < 5; i++)
          {
            if (weight < pointranges[i]) //if weight is between this point and the point before its range
            {
              float dist_from_lower_point = weight - pointranges[i - 1];
              float size_of_point_range = pointranges[i] - pointranges[i - 1];

              float ratio_over_lower_point = dist_from_lower_point / size_of_point_range;

              //now with ratio or percentage (0-1) into the point range, multiply color ranges to get color

              float4 color_range = colors[i] - colors[i - 1];

              float4 color_contribution = color_range * ratio_over_lower_point;

              float4 new_color = colors[i - 1] + color_contribution;
              return new_color;

            }
          }
          return colors[0];
        }

        //start //new 
        float distsq(float2 a, float2 b)
        {
            float area_of_effect_size = _Diameter;
        
            float circular_dist = distance(a, b); // Calculate the circular distance
            float normalized_circular_dist = saturate(circular_dist / area_of_effect_size); // Normalize the circular distance
        
            return pow(max(0.0, 1.0 - normalized_circular_dist), 2.0); // Apply circular falloff
        }
        //end 

        fixed4 frag(v2f i) : SV_Target
        {
            initalize();
            float2 uv = i.uv;
            uv = uv * 4.0 - float2(2.0, 2.0);  //our texture uv range is -2 to 2

            float totalWeight = 0.0;

            for (float i = 0.0; i < _HitCount; i++)
            {
                float2 work_pt = float2(_Hits[i * 3], _Hits[i * 3 + 1]);
                float pt_intensity = _Hits[i * 3 + 2];
                totalWeight += 0.5 * distsq(uv, work_pt) * pt_intensity * _Strength * (1 + sin(_Time.y * _PulseSpeed));
            }
            // totalWeight= 0.5f;
            // Create a circular mask
            // float circleMask = step(length(uv), _Diameter * _circleDiameter);

            // // Discard fragments outside of the circular area
            // if (circleMask == 0.0)
            // {
            //     discard;
            // }

            // Return the heatmap color with full alpha
            return getHeatForPixel(totalWeight);
        }
        


        ENDCG
        // Color [_Color0]
      }
    }
}
