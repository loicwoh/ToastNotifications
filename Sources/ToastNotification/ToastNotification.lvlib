<?xml version='1.0' encoding='UTF-8'?>
<Library LVVersion="26008000">
	<Property Name="NI.Lib.Description" Type="Str">Windows toast composition, display and activation replies for LabVIEW. ToastSource defines the common source contract; ToastBuilder is its current concrete implementation. Create ToastSource (Poly) groups concrete constructors. ToastService manages native integration and ActivationHandler hooks; UserEventActivationHandler relays copied LabVIEW activation data. Toast Native and Reflection DotNet are implementation details. See the online API and ownership documentation for usage and current limits.</Property>
	<Property Name="NI.Lib.HelpPath" Type="Str"></Property>
	<Property Name="NI.Lib.Icon" Type="Bin">*A#!!!!!!!)!"1!&amp;!!!-!%!!!@````]!!!!"!!%!!!)H!!!*Q(C=\&gt;8"=?*!%)8BNVM_&lt;"5H-NACB5["&amp;&amp;!)H1*8DK41+:!#+&lt;Q53)%5P,_'"HPNMLH9LKUNDRA"&lt;[3?TS-B3[0^EB\U?+]NXGW8]7G;ZNXCNJMOU86]-&gt;V?F\@&amp;&gt;@^C`/GA.];\\02[`&amp;L[/P6@Y_`Y\T2^N_`W@\@&gt;X2`"J`]/@GB_%.&amp;.,XL31`/UDS9XO=F.&lt;H+4&amp;XG2&amp;XG2&amp;XG2*XG3*XG3*XG3"XG1"XG1"XG1DYV=Z#)8/31TO:H)&amp;$5&amp;T-&amp;1:(&lt;'9TT'9TR]F@%9D`%9D`&amp;QC)T(?)T(?)S(UW1]RG-]RG-]F"I3DYU=D`&amp;18I7H]"3?QF.YG&amp;+&amp;JQ!5ER7&amp;CS)Q6!Q7(QJ0Y3E]@&amp;4B+4S&amp;J`!5(I:6?!J0Y3E]B9&gt;4RKL5U-Q&lt;/2\++0%EHM34?")0J:6Y%E`C34S*B_G5?"*0AEAG4)J$5(*3=E$S*@%E(N[5?"*0YEE]C9?B=96SL-SMG4&gt;S0)%H]!3?Q".Y++(!%XA#4_!*0*26Y!E]A3@Q""[G5O!*0)%HA!34-LW#9M'*Q5&amp;"%(BYD&lt;MFRF7K)9GR38XTKG^+^=WGPIH5.Y@[IKMPJPICK2&gt;@P;DKR6)PAPK05[06'05E[J0H!X6G@[)@[1@[HL[F&lt;_BL_IK_H%`^Y!00Z\./JZ//R[-/BY0W_\WWW[UWGYX7[\67KZ77S_8N-@#&lt;\@:!O$S8&gt;HR_KX`"`_&gt;`Y.GIHXI_"WPU"SGW(4-!!!!!</Property>
	<Property Name="NI.Lib.LocalName" Type="Str">ToastNotification</Property>
	<Property Name="NI.Lib.SourceVersion" Type="Int">637566976</Property>
	<Property Name="NI.Lib.Version" Type="Str">1.0.0.0</Property>
	<Property Name="NI.Lib.VIIconTemplate" Type="Str">50 54 51 49 56 48 48 49 13 0 0 0 0 1 23 21 76 111 97 100 32 38 32 85 110 108 111 97 100 46 108 118 99 108 97 115 115 0 0 1 0 0 0 0 0 9 0 0 4 46 1 100 1 100 80 84 72 48 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 15 13 76 97 121 101 114 46 108 118 99 108 97 115 115 0 0 1 0 0 0 0 0 7 0 0 3 189 0 0 0 0 0 0 0 0 0 0 3 162 0 40 0 0 3 156 0 0 3 96 0 0 0 0 0 9 0 32 0 24 0 0 0 0 0 255 255 255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 0 0 0 0 0 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 0 0 0 0 0 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 0 0 0 0 0 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 0 0 0 0 0 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 0 0 0 0 0 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 0 0 0 0 0 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 255 204 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 255 0 0 0 7 86 73 32 73 99 111 110 100 1 0 0 0 0 0 5 84 79 65 83 84 0 0 0 0 0 0 0 0 0 0 0 0 0 150 150 150 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 11 83 109 97 108 108 32 70 111 110 116 115 0 1 8 1 1

</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Property Name="NI.SortType" Type="Int">3</Property>
	<Item Name="Bins" Type="Folder">
		<Item Name="Microsoft.Toolkit.Uwp.Notifications.dll" Type="Document" URL="../../bins/Microsoft.Toolkit.Uwp.Notifications.dll"/>
	</Item>
	<Item Name="Support" Type="Folder">
		<Item Name="Reflection DotNet.lvlib" Type="Library" URL="../../Reflection DotNet/Reflection DotNet.lvlib"/>
		<Item Name="Toast Native.lvlib" Type="Library" URL="../../Toast Native/Toast Native.lvlib"/>
	</Item>
	<Item Name="ActivationHandler" Type="Folder">
		<Item Name="ActivationHandler.lvclass" Type="LVClass" URL="../../ActivationHandler/ActivationHandler.lvclass"/>
		<Item Name="UserEventActivationHandler.lvclass" Type="LVClass" URL="../../PlugIns/UserEventActivationHandler/UserEventActivationHandler.lvclass"/>
	</Item>
	<Item Name="ToastSource" Type="Folder">
		<Item Name="Create ToastSource (Poly).vi" Type="VI" URL="../Create ToastSource (Poly).vi"/>
		<Item Name="ToastBuilder.lvclass" Type="LVClass" URL="../../ToastBuilder/ToastBuilder.lvclass"/>
		<Item Name="ToastFromXML.lvclass" Type="LVClass" URL="../../ToastFromXML/ToastFromXML.lvclass"/>
		<Item Name="ToastSource.lvclass" Type="LVClass" URL="../../ToastSource/ToastSource.lvclass"/>
	</Item>
	<Item Name="Typedefs" Type="Folder">
		<Item Name="Activation.ctl" Type="VI" URL="../Activation.ctl"/>
		<Item Name="Argument.ctl" Type="VI" URL="../Argument.ctl"/>
	</Item>
	<Item Name="ToastService.lvclass" Type="LVClass" URL="../../ToastService/ToastService.lvclass"/>
</Library>
