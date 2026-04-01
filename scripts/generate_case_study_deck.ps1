$ErrorActionPreference = 'Stop'

$primaryOutputPath = Join-Path $PSScriptRoot '..\CallSenseAI_Case_Study_Deck.pptx'
$primaryOutputPath = [System.IO.Path]::GetFullPath($primaryOutputPath)
$fallbackOutputPath = Join-Path $PSScriptRoot '..\CallSenseAI_Case_Study_Deck_v2.pptx'
$fallbackOutputPath = [System.IO.Path]::GetFullPath($fallbackOutputPath)
$outputPath = $primaryOutputPath

function Set-TextStyle {
    param(
        $range,
        [int]$size,
        [string]$fontName,
        [int]$rgb,
        [bool]$bold = $false
    )

    $range.Font.Name = $fontName
    $range.Font.Size = $size
    $range.Font.Bold = [int]($bold)
    $range.Font.Color.RGB = $rgb
}

function Add-Banner {
    param($slide, [float]$width)
    $banner = $slide.Shapes.AddShape(1, 0, 0, $width, 24)
    $banner.Fill.ForeColor.RGB = 0x88940D
    $banner.Line.Visible = 0
}

function Add-Brand {
    param(
        $slide,
        [float]$width,
        [int]$rgb
    )

    $brand = $slide.Shapes.AddTextbox(1, $width - 124, 12, 96, 18)
    $brand.TextFrame.TextRange.Text = 'AscendX'
    Set-TextStyle -range $brand.TextFrame.TextRange -size 11 -fontName 'Aptos' -rgb $rgb -bold $true
    $brand.TextFrame.TextRange.ParagraphFormat.Alignment = 3
    $brand.Line.Visible = 0
    $brand.Fill.Visible = 0
}

$slides = @(
    @{
        Layout = 1
        Title = 'From Business Problem to Clear Requirements'
        Body = 'A Practical Framework Using a Real Case Study' + "`r`n" + 'Presented by: Kingsley Ohere'
    },
    @{
        Layout = 2
        Title = 'The Scenario'
        Body = @(
            'A company is facing two issues:'
            '- Sales are declining'
            '- Customer reviews are getting worse'
            ''
            'Leadership asks:'
            '"Can we build a dashboard or AI system to fix this?"'
            ''
            'Question:'
            'Build immediately, or understand the problem first?'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'The Common Mistake'
        Body = @(
            'Jumping straight into solutions'
            '- Building dashboards too early'
            '- Applying AI without clarity'
            '- Solving symptoms, not the real problem'
            ''
            'Result: wasted time, wrong solutions, poor outcomes'
            ''
            'Discussion: Why is this risky?'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'A Simple Framework'
        Body = @(
            'How do we approach this properly?'
            '1. Clarify the business problem'
            '2. Identify stakeholders'
            '3. Break into requirements'
            '4. Define success metrics'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'Step 1: Clarify the Problem'
        Body = @(
            'Start with the right question'
            '"Sales are dropping" is a symptom.'
            'Ask why:'
            '- Are customers leaving?'
            '- Is conversion declining?'
            '- Is customer experience poor?'
            ''
            'Goal: move from vague to specific.'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'Step 2: Identify Stakeholders'
        Body = @(
            'Who is impacted by this problem?'
            '- Customer Support Team'
            '- Sales Team'
            '- Product Team'
            '- Leadership'
            ''
            'Key insight: each stakeholder sees a different version of the problem.'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'Step 3: Break into Requirements'
        Body = @(
            'Translate the problem into actionable needs'
            '- Visibility into customer complaints'
            '- Tracking of call outcomes'
            '- Understanding customer intent'
            '- Identifying friction points'
            ''
            'Focus: what do we need to know or build?'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'Step 4: Define Success Metrics'
        Body = @(
            'How do we measure improvement?'
            '- Reduced customer complaints'
            '- Increased customer retention'
            '- Improved satisfaction scores'
            '- Better call outcomes'
            ''
            'If we cannot measure it, we cannot improve it.'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'Case Study: CallSense-AI'
        Body = @(
            'Real-world application of the framework'
            'Initial situation:'
            '- Declining sales'
            '- Negative customer feedback'
            '- Increasing support pressure'
            ''
            'Core question: what is actually driving dissatisfaction and churn?'
        ) -join "`r`n"
        Tag = 'CallSense-AI case study'
    },
    @{
        Layout = 2
        Title = 'Case Walkthrough'
        Body = @(
            'Problem refinement'
            '- From: "Sales are dropping"'
            '- To: "Customer churn linked to poor support interactions"'
            ''
            'Key discovery'
            '- 6 intent archetypes discovered from call transcripts'
            '- Subscription cancellation calls drove 38% of escalations while representing roughly 25% of volume'
            '- Technical support talk-ratio overload exposed about $3.4k/month in avoidable cost'
            ''
            'Requirements identified'
            '- Analyze conversations'
            '- Detect call intent'
            '- Identify recurring friction'
            '- Generate actionable business insights'
        ) -join "`r`n"
        Tag = 'CallSense-AI case study'
    },
    @{
        Layout = 2
        Title = 'Business Impact'
        Body = @(
            'Shift from data to decisions'
            'Instead of only viewing dashboards, the team could:'
            '- Understand why customers were unhappy'
            '- Pinpoint root causes behind churn and escalations'
            '- Prioritize the highest-risk call archetypes'
            '- Protect privacy with PII redaction before downstream NLP'
            ''
            'Enabling stack: MPNet embeddings, UMAP + HDBSCAN clustering, BART zero-shot intent labeling, BERT-NER redaction'
        ) -join "`r`n"
        Tag = 'CallSense-AI case study'
    },
    @{
        Layout = 2
        Title = 'Quick Discussion'
        Body = @(
            'Think like a Business Analyst'
            'Question: what is one key question you would ask before building any solution here?'
            ''
            'Follow-up: what would you validate first before committing resources?'
        ) -join "`r`n"
    },
    @{
        Layout = 2
        Title = 'Key Takeaways'
        Body = @(
            '- Business problems must be clearly defined'
            '- Symptoms are not the real problem'
            '- Requirements guide the right solution'
            '- Success must be measurable'
            '- Good analysis leads to better decisions'
            ''
            'Final question: what would you do differently next time before jumping into a solution?'
        ) -join "`r`n"
    }
)

$powerPoint = $null
$presentation = $null

try {
    $powerPoint = New-Object -ComObject PowerPoint.Application
    $powerPoint.Visible = -1
    $presentation = $powerPoint.Presentations.Add()

    $width = $presentation.PageSetup.SlideWidth
    $height = $presentation.PageSetup.SlideHeight

    foreach ($item in $slides) {
        $layout = $presentation.SlideMaster.CustomLayouts.Item($item.Layout)
        $slide = $presentation.Slides.AddSlide($presentation.Slides.Count + 1, $layout)

        if ($item.Layout -eq 1) {
            $slide.FollowMasterBackground = $false
            $slide.Background.Fill.ForeColor.RGB = 0x88940D
            Add-Brand -slide $slide -width $width -rgb 0xFFFFFF | Out-Null

            $titleRange = $slide.Shapes.Title.TextFrame.TextRange
            $titleRange.Text = $item.Title
            Set-TextStyle -range $titleRange -size 26 -fontName 'Aptos Display' -rgb 0xFFFFFF -bold $true

            $subShape = $slide.Shapes.Placeholders.Item(2)
            $subRange = $subShape.TextFrame.TextRange
            $subRange.Text = $item.Body
            Set-TextStyle -range $subRange -size 18 -fontName 'Aptos' -rgb 0xF2F2F2
        }
        else {
            $slide.FollowMasterBackground = $false
            $slide.Background.Fill.ForeColor.RGB = 0xFAFCF8
            Add-Banner -slide $slide -width $width | Out-Null
            Add-Brand -slide $slide -width $width -rgb 0x115E59 | Out-Null

            $titleRange = $slide.Shapes.Title.TextFrame.TextRange
            $titleRange.Text = $item.Title
            Set-TextStyle -range $titleRange -size 24 -fontName 'Aptos Display' -rgb 0x2F2F2F -bold $true

            $bodyShape = $slide.Shapes.Placeholders.Item(2)
            $bodyRange = $bodyShape.TextFrame.TextRange
            $bodyRange.Text = $item.Body
            Set-TextStyle -range $bodyRange -size 18 -fontName 'Aptos' -rgb 0x2F2F2F
            $bodyShape.TextFrame.WordWrap = -1

            if ($item.ContainsKey('Tag')) {
                $tag = $slide.Shapes.AddTextbox(1, $width - 180, 34, 150, 20)
                $tag.TextFrame.TextRange.Text = $item.Tag
                Set-TextStyle -range $tag.TextFrame.TextRange -size 10 -fontName 'Aptos' -rgb 0x88940D -bold $true
                $tag.Line.Visible = 0
                $tag.Fill.Visible = 0
            }

            $footer = $slide.Shapes.AddTextbox(1, 24, $height - 28, 280, 16)
            $footer.TextFrame.TextRange.Text = 'CallSense-AI teaching deck'
            Set-TextStyle -range $footer.TextFrame.TextRange -size 9 -fontName 'Aptos' -rgb 0x64748B
            $footer.Line.Visible = 0
            $footer.Fill.Visible = 0
        }
    }

    if (Test-Path -LiteralPath $primaryOutputPath) {
        try {
            Remove-Item -LiteralPath $primaryOutputPath -Force
        }
        catch {
            $outputPath = $fallbackOutputPath
        }
    }

    $presentation.SaveAs($outputPath)
}
finally {
    if ($presentation -ne $null) {
        $presentation.Close()
    }
    if ($powerPoint -ne $null) {
        $powerPoint.Quit()
    }
}

Write-Output "Created $outputPath"
