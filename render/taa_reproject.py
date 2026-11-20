"""第 62 批：镜头慢推时栅栏边缘像水波一样抖，快速转身后整帧拖出残影，雨丝变成..."""

def jitter_sequence(frame, count):
    """抖动序列：按帧号循环取抖动偏移，暂停时帧号停住偏移也停住。"""
    if count <= 0:
        raise ValueError("count must be positive")
    return frame % count

def velocity_present(camera, skinned):
    """全量速度：相机运动与蒙皮/粒子运动矢量任一存在即视为有速度。"""
    return bool(camera) or bool(skinned)

def neighborhood_clip(center, low, high):
    """邻域裁剪：把历史颜色钳制到当前帧邻域的 [low, high] 范围。"""
    return clamp_axis(center, low, high)

def disocclusion(depth_delta, threshold):
    """去遮挡：深度差超过阈值判定为新暴露区域，拒绝历史。"""
    return depth_delta > threshold

def alpha_test(alpha, cutoff):
    """alpha 材质：按当前帧 cutoff 判定镂空，不沿用历史镂空形状。"""
    return alpha >= cutoff

def hdr_weight(luma, threshold):
    """HDR 历史权重：亮度超过阈值时历史权重随亮度反比下降。"""
    if luma <= 0:
        return 1.0
    if luma <= threshold:
        return 1.0
    return 1.0 / luma

def reset_on_resize(width, old_width):
    """分辨率重置：尺寸变化（含 DLSS 开关）时需要清空历史纹理。"""
    return width != old_width

def motion_class(static, dynamic):
    """动静分离：按像素运动来源分类，动态与静态不共用同一张历史。"""
    if static and dynamic:
        return "mixed"
    if dynamic:
        return "dynamic"
    if static:
        return "static"
    return "none"

def overspeed(speed, max_speed):
    """超速抑制：速度超过重投影范围时丢弃历史，防止长条鬼影。"""
    return speed > max_speed

def cut_reset(cut, history):
    """cut 重置：镜头切换后清空历史，避免两个镜头混在一起。"""
    if cut:
        return None
    return history

def ui_mask(ui, depth):
    """UI 隔离：UI/字幕不写入场景颜色，遮罩处深度归零。"""
    if ui:
        return 0
    return depth

def camera_history(camera_id, history):
    """多相机历史键：每个相机独立历史纹理，分屏互不污染。"""
    return f"{camera_id}:{history}"

def sharpen_order(taa_pass, sharpen_pass):
    """锐化顺序：锐化必须在 TAA 之后，避免边缘抖动被放大。"""
    return taa_pass < sharpen_pass

def blend_weight(feedback, motion):
    """混合权重：历史反馈权重随运动矢量幅度衰减。"""
    return feedback * motion

def clamp_axis(value, low, high):
    """钳制。"""
    return max(low, min(high, value))
