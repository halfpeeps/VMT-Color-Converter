if CLIENT then
    local boostFactor = 2.1

    local function PerceptualToColor2(r, g, b, boost)
        boost = boost or boostFactor
        local function adjust(c)
            local normalized = c / 255
            local boosted = math.pow(normalized, 1 / boost)
            return math.Round(math.min(boosted, 1.0), 3)
        end
        return adjust(r), adjust(g), adjust(b)
    end

    local function Color2ToPerceptual(r, g, b, boost)
        boost = boost or boostFactor
        local function reverse(c)
            local boosted = math.pow(c, boost) * 255
            return math.Clamp(math.Round(boosted), 0, 255)
        end
        return reverse(r), reverse(g), reverse(b)
    end

    local function OpenColorConverter()
        local frame = vgui.Create("DFrame")
        frame:SetTitle("VMT $color Converter")
        frame:SetSize(460, 360)
        frame:Center()
        frame:MakePopup()

        local label = vgui.Create("DLabel", frame)
        label:SetText("$color2 → $color:")
        label:SetPos(30, 35)
        label:SizeToContents()

        local rEntry = vgui.Create("DTextEntry", frame)
        rEntry:SetNumeric(true)
        rEntry:SetPlaceholderText("R (0-255)")
        rEntry:SetPos(30, 60)
        rEntry:SetSize(120, 25)

        local gEntry = vgui.Create("DTextEntry", frame)
        gEntry:SetNumeric(true)
        gEntry:SetPlaceholderText("G (0-255)")
        gEntry:SetPos(165, 60)
        gEntry:SetSize(120, 25)

        local bEntry = vgui.Create("DTextEntry", frame)
        bEntry:SetNumeric(true)
        bEntry:SetPlaceholderText("B (0-255)")
        bEntry:SetPos(300, 60)
        bEntry:SetSize(120, 25)

        local result = vgui.Create("DTextEntry", frame)
        result:SetEditable(false)
        result:SetPos(30, 100)
        result:SetSize(390, 25)

        local function update()
            local r = tonumber(rEntry:GetValue()) or 0
            local g = tonumber(gEntry:GetValue()) or 0
            local b = tonumber(bEntry:GetValue()) or 0
            r, g, b = math.Clamp(r, 0, 255), math.Clamp(g, 0, 255), math.Clamp(b, 0, 255)
            local cr, cg, cb = PerceptualToColor2(r, g, b)
            result:SetText(string.format('$color2 "[%.3f %.3f %.3f]"', cr, cg, cb))
        end

        local convertBtn = vgui.Create("DButton", frame)
        convertBtn:SetText("Convert to $color2")
        convertBtn:SetPos(30, 135)
        convertBtn:SetSize(390, 30)
        convertBtn.DoClick = update

        local boostLabel = vgui.Create("DLabel", frame)
        boostLabel:SetText("Boost Factor:")
        boostLabel:SetPos(30, 180)
        boostLabel:SizeToContents()

        local boostSlider = vgui.Create("DNumSlider", frame)
        boostSlider:SetPos(30, 200)
        boostSlider:SetSize(390, 40)
        boostSlider:SetMin(1)
        boostSlider:SetMax(3)
        boostSlider:SetDecimals(2)
        boostSlider:SetValue(boostFactor)
        boostSlider:SetText("")
        boostSlider:SetTooltip("How much the intensity is altered in order to maintain\na percieved consistency in colour between shaders.\n(Default: 2.1)")

        boostSlider.OnValueChanged = function(_, val)
            boostFactor = val
            update()
        end

        local label2 = vgui.Create("DLabel", frame)
        label2:SetText("Reverse calculation ($color2 → $color)")
        label2:SetPos(30, 250)
        label2:SizeToContents()

        local crEntry = vgui.Create("DTextEntry", frame)
        crEntry:SetPlaceholderText("R (0-1)")
        crEntry:SetPos(30, 275)
        crEntry:SetSize(120, 25)

        local cgEntry = vgui.Create("DTextEntry", frame)
        cgEntry:SetPlaceholderText("G (0-1)")
        cgEntry:SetPos(165, 275)
        cgEntry:SetSize(120, 25)

        local cbEntry = vgui.Create("DTextEntry", frame)
        cbEntry:SetPlaceholderText("B 0-1")
        cbEntry:SetPos(300, 275)
        cbEntry:SetSize(120, 25)

        local reverseBtn = vgui.Create("DButton", frame)
        reverseBtn:SetText("Convert to $color")
        reverseBtn:SetPos(30, 310)
        reverseBtn:SetSize(390, 30)
        reverseBtn.DoClick = function()
            local r = tonumber(crEntry:GetValue()) or 0
            local g = tonumber(cgEntry:GetValue()) or 0
            local b = tonumber(cbEntry:GetValue()) or 0
            r, g, b = math.Clamp(r, 0, 1), math.Clamp(g, 0, 1), math.Clamp(b, 0, 1)
            local pr, pg, pb = Color2ToPerceptual(r, g, b)
            rEntry:SetText(pr)
            gEntry:SetText(pg)
            bEntry:SetText(pb)
            update()
        end

        result.OnChange = updateVMT
    end

    concommand.Add("open_color_converter", OpenColorConverter)
end
