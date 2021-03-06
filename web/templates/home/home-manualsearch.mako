<%!
    import autosubliminal
%>

<div class="container">

    <div class="panel panel-default">

        <div class="panel-heading">
            <span class="panel-title badge">Found subtitles (${len(subs)})</span>
        </div>

        % if len(subs) >= 1:

            <div class="panel-body">

                <table class="table">

                    <thead>
                    <tr>
                        <th>Score</th>
                        <th>Provider</th>
                        <th>Preview</th>
                        <th>Actions</th>
                    </tr>
                    </thead>

                    <tbody>
                        % for index, sub in enumerate(subs):
                            <tr>
                                <td class="text-left">${sub['score']}</td>
                                <td>
                                    <span class="dropdown">
                                        <span class="dropdown-toggle dropdown-hoverintent" data-toggle="dropdown" data-hover="dropdown">
                                            ${sub['provider_name']}
                                        </span>
                                        <ul class="dropdown-menu has-tip info-list">
                                            <li>
                                                <span class="info-list-label">Supported releases:</span>
                                                <ul>
                                                    % for release in sub['releases']:
                                                        <li>${release}</li>
                                                    % endfor
                                                </ul>
                                            </li>
                                        </ul>
                                    </span>
                                </td>
                                <td class="text-left">
                                    <div class="subtitle-preview">${sub['content_preview']}</div>
                                </td>
                                <td class="text-center">
                                    <a class="subtitle-action manualsearchvisitlink" href="${autosubliminal.DEREFERURL}${sub['page_link']}">
                                        <i class="fa fa-arrow-circle-right" aria-hidden="true" title="Click to visit website"></i>
                                    </a>
                                    <br>
                                    <a class="subtitle-action manualsearchsavelink" href="${autosubliminal.WEBROOT}/home/saveSubtitle/${sub['wanted_item_index']}/${sub['subtitle_index']}">
                                        <i class="fa fa-floppy-o" aria-hidden="true" title="Click to save subtitle"></i>
                                    </a>
                                    <br>
                                    <a class="subtitle-action manualsearchdeletelink" href="${autosubliminal.WEBROOT}/home/deleteSubtitle/${sub['wanted_item_index']}">
                                        <i class="fa fa-times" aria-hidden="true" title="Click to delete subtitle"></i>
                                    </a>
                                    <br>
                                    <a class="subtitle-action manualsearchplaylink" href="${sub['playvideo_url']}">
                                        <i class="fa fa-play-circle-o" aria-hidden="true" title="Click to play video"></i>
                                    </a>
                                    <br>
                                    <a class="subtitle-action manualsearchpostprocesslink" href="${autosubliminal.WEBROOT}/home/postProcess/${sub['wanted_item_index']}/${sub['subtitle_index']}">
                                        <i class="fa fa-refresh" aria-hidden="true" title="Click to execute post processing"></i>
                                        <i class="fa fa-refresh fa-spin hidden" aria-hidden="true" title="Post processing..."></i>
                                    </a>
                                    <br>
                                </td>
                            </tr>
                        % endfor
                    </tbody>

                </table>

            </div>

        % endif

        <div class="panel-footer">
            <div id="div-error" class="bg-danger">${errormessage if errormessage else ''}</div>
            <div id="div-info" class="bg-info">${infomessage if infomessage else ''}</div>
        </div>

    </div>

</div>

<!-- Need to include it here because otherwise it's loaded too early which causes some functionality to fail -->
<script type="text/javascript" src="${autosubliminal.WEBROOT}/js/home-manualsearch.js?v=${appUUID}"></script>
